import os
import logging

logger = logging.getLogger(__name__)

USER_DEFAULT_PHONE = "+919704638232"

def format_phone_number(phone: str = None) -> str:
    """
    Formats phone numbers into standard E.164 international format (+919704638232).
    Defaults to +919704638232 if unspecified.
    """
    if not phone:
        return os.getenv("EMERGENCY_PHONE_NUMBER") or USER_DEFAULT_PHONE
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    if len(phone) == 10 and phone.isdigit():
        return f"+91{phone}"
    if not phone.startswith("+"):
        return f"+{phone}"
    return phone

def send_emergency_sms(message_body: str, recipient_phone: str = None) -> dict:
    """
    Dispatches emergency SMS notification using Twilio API to target number (+919704638232).
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    to_phone = format_phone_number(recipient_phone)

    if not account_sid or not auth_token or not from_phone:
        logger.info(f"[Twilio SMS] Credentials missing in environment. Mock SMS to {to_phone}: {message_body}")
        return {
            "status": "MOCK_DISPATCHED",
            "to": to_phone,
            "message": f"Twilio credentials missing in .env. Simulated emergency SMS logged for {to_phone}.",
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
    Initiates an emergency phone call alert using Twilio Voice API to target number (+919704638232).
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    target_phone = format_phone_number(to_phone)

    reason_text = alert_reason or "high risk driver status detected"
    twiml_payload = f'<Response><Say voice="alice">Emergency Driver Alert! SmartRoad AI has detected {reason_text}. Immediate attention required for driver safety.</Say></Response>'

    if not account_sid or not auth_token or not from_phone:
        logger.info(f"[Twilio Voice] Credentials missing in environment. Mock Call to {target_phone} ({reason_text})")
        return {
            "status": "MOCK_CALL_INITIATED",
            "to": target_phone,
            "message": f"High Risk Twilio Call Triggered to {target_phone} (Simulated mode). Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, & TWILIO_PHONE_NUMBER to backend/.env to place live phone calls to {target_phone}.",
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
