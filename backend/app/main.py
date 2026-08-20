from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.telemetry import router as telemetry_router
from app.api.session import router as session_router
from app.api.profile import router as profile_router
from app.api.vehicle import router as vehicle_router
from app.api.emergency import router as emergency_router

from app.db.session import engine, Base
import app.models.user
import app.models.telemetry
import app.models.session
import app.models.profile
import app.models.vehicle
import app.models.emergency

# Create tables automatically for local/SQLite dev
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Database metadata creation skipped or failed:", e)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(telemetry_router, prefix=settings.API_V1_STR)
app.include_router(session_router, prefix=settings.API_V1_STR)
app.include_router(profile_router, prefix=settings.API_V1_STR)
app.include_router(vehicle_router, prefix=settings.API_V1_STR)
app.include_router(emergency_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartRoad AI Telemetry & Emergency Response Service"}
