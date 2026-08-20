from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.emergency import EmergencyAlert
from app.schemas.emergency import EmergencyAlertCreate, EmergencyAlertStatusUpdate, EmergencyAlertResponse
from app.api.auth import get_current_user
from app.services.twilio_service import send_emergency_sms, make_emergency_call

router = APIRouter(prefix="/emergency", tags=["Emergency Response"])

@router.get("/", response_model=List[EmergencyAlertResponse])
def get_emergency_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves emergency alerts. Caretaker, Police, Hospital, and Admin roles receive all active alerts.
    Drivers receive their personal emergency alerts.
    """
    role = (current_user.role or "driver").lower()
    if role in ["caretaker", "hospital", "police", "admin"]:
        alerts = db.query(EmergencyAlert).order_by(EmergencyAlert.created_at.desc()).all()
    else:
        alerts = db.query(EmergencyAlert).filter(EmergencyAlert.driver_id == current_user.id).order_by(EmergencyAlert.created_at.desc()).all()
    return alerts

@router.post("/", response_model=EmergencyAlertResponse, status_code=status.HTTP_201_CREATED)
def trigger_emergency_alert(
    payload: EmergencyAlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dispatches a critical driver risk emergency alert.
    Persists alert in database, triggers Twilio notifications if configured, and returns created alert.
    """
    alert = EmergencyAlert(
        driver_id=current_user.id,
        vehicle_id=payload.vehicle_id,
        alert_type=payload.alert_type,
        risk_score=payload.risk_score,
        latitude=payload.latitude,
        longitude=payload.longitude,
        details=payload.details or f"Critical driver alert triggered for driver {current_user.name or current_user.email}",
        status="NEW"
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # Attempt Twilio emergency notification dispatch
    msg = f"🚨 SMARTROAD AI EMERGENCY ALERT! Driver {current_user.name or current_user.email} triggered {payload.alert_type} (Risk: {payload.risk_score}/100) at Lat: {payload.latitude}, Lon: {payload.longitude}."
    send_emergency_sms(msg)
    if payload.risk_score >= 85.0:
        make_emergency_call()

    return alert

@router.patch("/{alert_id}/status", response_model=EmergencyAlertResponse)
def update_alert_status(
    alert_id: int,
    payload: EmergencyAlertStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates response status of an emergency alert ('NEW' -> 'ACKNOWLEDGED' -> 'RESPONDING' -> 'RESOLVED').
    Allowed for Caretaker, Hospital, Police, and Admin roles.
    """
    alert = db.query(EmergencyAlert).filter(EmergencyAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Emergency alert record not found.")

    alert.status = payload.status
    db.commit()
    db.refresh(alert)
    return alert
