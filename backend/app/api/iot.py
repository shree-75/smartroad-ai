from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Any
import time

from app.db.session import get_db
from app.models.iot import IoTTelemetry
from app.schemas.iot import IoTTelemetryCreate, IoTTelemetryResponse, IoTStatusResponse
from app.api.telemetry import broadcast_telemetry_update

router = APIRouter(prefix="/iot", tags=["IoT Hardware Telemetry"])

# Global Memory State for ESP32 Connection Heartbeat
LAST_IOT_HEARTBEAT_TIME = 0.0
LAST_IOT_DATA = None

@router.post("/telemetry", response_model=IoTTelemetryResponse, status_code=status.HTTP_201_CREATED)
def post_iot_telemetry(payload: IoTTelemetryCreate, db: Session = Depends(get_db)):
    """
    Receives JSON telemetry directly from ESP32 hardware or test scripts.
    Persists data in SQLite and broadcasts to active WebSockets.
    """
    global LAST_IOT_HEARTBEAT_TIME, LAST_IOT_DATA

    now_ts = time.time()
    LAST_IOT_HEARTBEAT_TIME = now_ts

    sensor_map = payload.sensors or {
        "max30102": "ONLINE" if payload.heart_rate is not None else "OFFLINE",
        "mpu6050": "ONLINE",
        "alcohol": "ONLINE" if payload.alcohol is not None else "OFFLINE",
        "vibration": "ONLINE"
    }

    db_obj = IoTTelemetry(
        device_id=payload.device_id or "ESP32-001",
        session_id=payload.session_id,
        heart_rate=payload.heart_rate,
        spo2=payload.spo2,
        alcohol=payload.alcohol,
        vibration=payload.vibration or 0,
        acceleration_x=payload.acceleration_x or 0.0,
        acceleration_y=payload.acceleration_y or 0.0,
        acceleration_z=payload.acceleration_z or 1.0,
        gyro_x=payload.gyro_x or 0.0,
        gyro_y=payload.gyro_y or 0.0,
        gyro_z=payload.gyro_z or 0.0,
        sensor_statuses=sensor_map,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    res_dict = db_obj.to_dict()
    LAST_IOT_DATA = res_dict

    # Broadcast via WebSocket infrastructure
    broadcast_telemetry_update({
        "type": "iot_update",
        "iot_telemetry": res_dict,
        "connected": True,
        "last_seen_sec": 0.1
    })

    return res_dict

@router.get("/status", response_model=IoTStatusResponse)
def get_iot_status():
    """
    Returns real-time connection status of ESP32 based on actual packet heartbeat.
    """
    global LAST_IOT_HEARTBEAT_TIME, LAST_IOT_DATA

    now = time.time()
    if LAST_IOT_HEARTBEAT_TIME > 0:
        elapsed = now - LAST_IOT_HEARTBEAT_TIME
        connected = elapsed <= 5.0 # Packet received within last 5 seconds
    else:
        elapsed = None
        connected = False

    sensors = LAST_IOT_DATA.get("sensors", {}) if (connected and LAST_IOT_DATA) else {
        "max30102": "OFFLINE",
        "mpu6050": "OFFLINE",
        "alcohol": "OFFLINE",
        "vibration": "OFFLINE"
    }

    return {
        "connected": connected,
        "device_id": LAST_IOT_DATA.get("device_id", "ESP32-001") if LAST_IOT_DATA else "ESP32-001",
        "last_seen_sec": round(elapsed, 1) if elapsed is not None else None,
        "sensor_statuses": sensors
    }

@router.get("/latest", response_model=IoTTelemetryResponse)
def get_latest_iot_telemetry(db: Session = Depends(get_db)):
    """
    Returns the most recent ESP32 IoT telemetry record from database.
    """
    record = db.query(IoTTelemetry).order_by(IoTTelemetry.id.desc()).first()
    if not record:
        raise HTTPException(status_code=404, detail="No IoT telemetry records found")
    return record.to_dict()

@router.get("/history", response_model=List[IoTTelemetryResponse])
def get_iot_telemetry_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    Returns recent IoT telemetry history log for graph rendering.
    """
    records = db.query(IoTTelemetry).order_by(IoTTelemetry.id.desc()).limit(limit).all()
    return [r.to_dict() for r in reversed(records)]
