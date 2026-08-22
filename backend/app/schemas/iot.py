from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class IoTTelemetryCreate(BaseModel):
    device_id: Optional[str] = "ESP32-001"
    session_id: Optional[str] = None
    timestamp: Optional[str] = None
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    alcohol: Optional[float] = None
    vibration: Optional[int] = 0
    acceleration_x: Optional[float] = 0.0
    acceleration_y: Optional[float] = 0.0
    acceleration_z: Optional[float] = 1.0
    gyro_x: Optional[float] = 0.0
    gyro_y: Optional[float] = 0.0
    gyro_z: Optional[float] = 0.0
    sensors: Optional[Dict[str, str]] = None

class IoTTelemetryResponse(BaseModel):
    id: int
    device_id: str
    session_id: Optional[str] = None
    timestamp: Optional[str] = None
    heart_rate: Optional[float] = None
    spo2: Optional[float] = None
    alcohol: Optional[float] = None
    vibration: int
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    sensors: Dict[str, str]
    created_at: str

    class Config:
        from_attributes = True

class IoTStatusResponse(BaseModel):
    connected: bool
    device_id: str
    last_seen_sec: Optional[float] = None
    sensor_statuses: Dict[str, str]
