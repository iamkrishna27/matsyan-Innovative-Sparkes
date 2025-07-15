from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, fishing, weather, sos
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartNavFish API",
    description="AI-Powered Navigation for Sustainable Fishing",
    version="1.0.0",
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(fishing.router, prefix="/fishing", tags=["fishing"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(sos.router, prefix="/emergency", tags=["emergency"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartNavFish API"}