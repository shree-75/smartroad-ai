import os
import logging

logger = logging.getLogger(__name__)

def send_emergency_sms(message_body: str, recipient_phone: str = None) -> dict:
    """
    Dispatches emergency SMS notification using Twilio API.
    Reads credentials strictly from environment variables.
    Returns status dict without crashing if Twilio is not configured.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    to_phone = recipient_phone or os.getenv("EMERGENCY_PHONE_NUMBER") or "+18005550199"

    if not account_sid or not auth_token or not from_phone:
        logger.info(f"[Twilio SMS] Credentials missing in environment. Mock SMS to {to_phone}: {message_body}")
        return {
            "status": "MOCK_DISPATCHED",
            "to": to_phone,
            "message": f"Twilio credentials missing. Simulated SMS logged for {to_phone}.",
            "sms_body": message_body
        }

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_phone,
            to=to_phone
        )
        logger.info(f"[Twilio SMS] Emergency SMS sent! SID: {message.sid} to {to_phone}")
        return {
            "status": "SENT",
            "sid": message.sid,
            "to": to_phone,
            "message": f"Emergency SMS dispatched successfully to {to_phone}"
        }
    except Exception as err:
        logger.error(f"[Twilio SMS Error] {err}")
        return {
            "status": "FAILED",
            "to": to_phone,
            "message": f"Twilio SMS Error: {str(err)}"
        }

def make_emergency_call(to_phone: str = None, alert_reason: str = None) -> dict:
    """
    Initiates an emergency phone call alert using Twilio Voice API.
    Returns status dict without crashing if credentials are missing.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    target_phone = to_phone or os.getenv("EMERGENCY_PHONE_NUMBER") or "+18005550199"

    reason_text = alert_reason or "high risk driver status detected"
    twiml_payload = f'<Response><Say voice="alice">Emergency Driver Alert! SmartRoad AI has detected {reason_text}. Immediate attention required for driver safety.</Say></Response>'

    if not account_sid or not auth_token or not from_phone:
        logger.info(f"[Twilio Voice] Credentials missing in environment. Mock Call to {target_phone} ({reason_text})")
        return {
            "status": "MOCK_CALL_INITIATED",
            "to": target_phone,
            "message": f"High Risk Twilio Call Triggered (Simulated mode to {target_phone}). Set TWILIO_ACCOUNT_SID & AUTH_TOKEN to make live calls.",
            "reason": reason_text
        }

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            twiml=twiml_payload,
            to=target_phone,
            from_=from_phone
        )
        logger.info(f"[Twilio Voice] Emergency call initiated! SID: {call.sid} to {target_phone}")
        return {
            "status": "CALL_INITIATED",
            "sid": call.sid,
            "to": target_phone,
            "message": f"Emergency voice call initiated successfully to {target_phone}"
        }
    except Exception as err:
        logger.error(f"[Twilio Voice Error] {err}")
        return {
            "status": "FAILED",
            "to": target_phone,
            "message": f"Twilio Voice Error: {str(err)}"
        }
