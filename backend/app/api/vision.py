import cv2
import sys
import time
import threading
import numpy as np
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse

# Add project root so ai.* imports work from backend context
sys.path.insert(0, "C:/Users/srini/smartroad-ai")

from ai.vision.camera import CameraStream
from ai.pipeline.driver_monitoring_engine import ResearchDriverMonitoringEngine
from app.services.twilio_service import make_emergency_call, send_emergency_sms

router = APIRouter(prefix="/vision", tags=["Vision Streaming"])

# ─────────────────────────────────────────────────────────────
# Singleton camera engine — shared across all browser clients
# ─────────────────────────────────────────────────────────────
class _CameraEngine:
    def __init__(self):
        self._camera  = None
        self._engine  = None
        self._lock    = threading.Lock()
        self._running = False
        self._latest_frame: bytes = b""
        self._last_twilio_call_time = 0.0
        self._last_twilio_status = "IDLE / READY"
        self._latest_metrics: dict = {
            "active": False,
            "person_count": 1,
            "face_detected": True,
            "driver_status": "normal",
            "phone_detected": False,
            "phone_status": "PHONE: NOT IN USE",
            "phone_reason": "",
            "phone_confidence": 0.0,
            "calling_detected": False,
            "drinking_detected": False,
            "drinking_status": "DRINKING: NOT DETECTED",
            "seatbelt_status": "SEATBELT DETECTED",
            "seatbelt_confidence": 0.85,
            "ear": 0.292,
            "left_ear": 0.290,
            "right_ear": 0.294,
            "mar": 0.185,
            "yaw": 0.0,
            "pitch": 0.0,
            "roll": 0.0,
            "head_orientation": "LOOKING_FORWARD",
            "posture_status": "NORMAL",
            "risk_score": 18,
            "risk_level": "LOW",
            "twilio_call_status": "IDLE / READY",
            "fps": 0.0
        }
        self._thread  = None

    def start(self):
        with self._lock:
            if self._running:
                return
            self._camera = CameraStream(camera_index=0, width=640, height=480)
            self._engine = ResearchDriverMonitoringEngine(calibration_duration_sec=30)
            self._running = True
            self._thread  = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        with self._lock:
            self._running = False
            if self._camera:
                self._camera.release()
                self._camera = None

    def _loop(self):
        while self._running:
            ret, frame = self._camera.read()
            if not ret:
                time.sleep(0.05)
                continue

            try:
                result = self._engine.process_frame(frame)
                annotated = result["frame"]

                fps_val = float(self._camera.fps) if self._camera else 0.0
                fps_text = f"FPS: {fps_val:.1f}"
                cv2.putText(annotated, fps_text, (annotated.shape[1] - 130, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                count = result.get("person_count", 0)
                cv2.putText(annotated, f"People: {count}",
                            (10, annotated.shape[0] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                m = result.get("metrics", {})
                s = result.get("score_info", {})
                
                phone_detected = bool(m.get("phone_detected", False))
                phone_status = str(m.get("phone_status", "PHONE: NOT IN USE"))
                phone_reason = str(m.get("phone_reason", ""))
                calling_detected = "CALLING" in phone_status or "HAND TO EAR" in phone_status
                risk_score = int(s.get("score", 18))
                risk_level = str(s.get("level", "LOW"))

                # 🚨 HIGH RISK TWILIO AUTOMATED EMERGENCY DISPATCH
                is_high_risk = risk_score >= 60 or risk_level in ["HIGH", "CRITICAL"] or phone_detected or calling_detected
                now = time.time()

                if is_high_risk and (now - self._last_twilio_call_time > 45.0):
                    self._last_twilio_call_time = now
                    reason = f"High Risk ({risk_score}/100) - {phone_status}" if phone_detected else f"High Driver Risk ({risk_score}/100)"
                    self._last_twilio_status = f"📞 CONNECTING TWILIO CALL ({reason})"

                    def _async_twilio_dispatch(r_text, score):
                        call_res = make_emergency_call(alert_reason=r_text)
                        sms_res = send_emergency_sms(f"🚨 SMARTROAD AI CRITICAL ALERT! Driver risk score is {score}/100. Event: {r_text}.")
                        status_str = call_res.get("status", "DISPATCHED")
                        msg = call_res.get("message", "Emergency Call Connect Triggered")
                        self._last_twilio_status = f"📞 {status_str}: {msg}"

                    threading.Thread(target=_async_twilio_dispatch, args=(reason, risk_score), daemon=True).start()

                metrics_snapshot = {
                    "active": True,
                    "person_count": count,
                    "face_detected": bool(result.get("face_detected", False)),
                    "driver_status": str(result.get("driver_status", "normal")),
                    "phone_detected": phone_detected,
                    "phone_status": phone_status,
                    "phone_reason": phone_reason,
                    "phone_confidence": float(m.get("phone_confidence", 0.0)),
                    "calling_detected": calling_detected,
                    "drinking_detected": bool(m.get("drinking_detected", False)),
                    "drinking_status": str(m.get("drinking_status", "DRINKING: NOT DETECTED")),
                    "seatbelt_status": str(m.get("seatbelt_status", "SEATBELT DETECTED")),
                    "seatbelt_confidence": float(m.get("seatbelt_confidence", 0.85)),
                    "ear": round(float(m.get("ear", 0.29)), 3),
                    "left_ear": round(float(m.get("left_ear", 0.29)), 3),
                    "right_ear": round(float(m.get("right_ear", 0.29)), 3),
                    "mar": round(float(m.get("mar", 0.18)), 3),
                    "yaw": round(float(m.get("yaw", 0.0)), 1),
                    "pitch": round(float(m.get("pitch", 0.0)), 1),
                    "roll": round(float(m.get("roll", 0.0)), 1),
                    "head_orientation": str(m.get("head_orientation", "LOOKING_FORWARD")),
                    "posture_status": str(m.get("posture_status", "NORMAL")),
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "twilio_call_status": self._last_twilio_status,
                    "fps": round(fps_val, 1)
                }

            except Exception as e:
                import traceback
                print(f"[VisionEngine Error] {e}")
                traceback.print_exc()
                annotated = frame
                metrics_snapshot = self._latest_metrics

            _, jpeg = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])
            with self._lock:
                self._latest_frame = jpeg.tobytes()
                self._latest_metrics = metrics_snapshot

    def get_frame(self) -> bytes:
        with self._lock:
            return self._latest_frame

    def get_metrics(self) -> dict:
        with self._lock:
            return dict(self._latest_metrics)


_engine = _CameraEngine()


# ─────────────────────────────────────────────────────────────
# MJPEG generator
# ─────────────────────────────────────────────────────────────
def _mjpeg_generator():
    _engine.start()
    boundary = b"--frame"
    while True:
        frame = _engine.get_frame()
        if frame:
            yield (
                boundary + b"\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame + b"\r\n"
            )
        time.sleep(0.033)   # ~30 fps cap


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────
@router.get("/stream")
def video_stream():
    """MJPEG live camera stream with face tracking overlay."""
    return StreamingResponse(
        _mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/metrics")
def camera_metrics():
    """Live computer vision telemetry metrics JSON."""
    _engine.start()
    return _engine.get_metrics()


@router.get("/status")
def camera_status():
    """Returns camera streaming status."""
    return {
        "status": "online" if _engine._running else "idle",
        "fps": getattr(_engine._camera, "fps", 0.0) if _engine._camera else 0.0,
        "view_url": "/api/v1/vision/view",
        "stream_url": "/api/v1/vision/stream",
        "metrics_url": "/api/v1/vision/metrics"
    }


@router.get("/view", response_class=HTMLResponse)
def camera_view():
    """Browser-friendly page showing the live tracking feed."""
    html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>SmartRoad AI — Live Face Tracker</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: 'Segoe UI', sans-serif;
      color: #e2e8f0;
    }
    h1 {
      font-size: 1.5rem;
      margin-bottom: 1rem;
      color: #06b6d4;
      letter-spacing: 0.1em;
    }
    .badge {
      display: inline-block;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 999px;
      padding: 4px 14px;
      font-size: 0.75rem;
      margin-bottom: 1.2rem;
      color: #94a3b8;
    }
    img {
      border-radius: 12px;
      border: 2px solid #06b6d4;
      max-width: 95vw;
      box-shadow: 0 0 40px rgba(6,182,212,0.25);
    }
    .legend {
      margin-top: 1rem;
      display: flex;
      gap: 24px;
      font-size: 0.82rem;
    }
    .legend span { display:flex; align-items:center; gap:6px; }
    .dot { width:12px; height:12px; border-radius:3px; }
    .cyan  { background:#06b6d4; }
    .orange{ background:#f97316; }
  </style>
</head>
<body>
  <h1>🚗 SmartRoad AI — Live Face Tracker</h1>
  <div class="badge">MJPEG · Real-time · Multi-face Detect + CSRT Track</div>
  <img src="/api/v1/vision/stream" alt="Live camera feed" />
  <div class="legend">
    <span><div class="dot cyan"></div> Primary Driver</span>
    <span><div class="dot orange"></div> Other Person</span>
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html)
