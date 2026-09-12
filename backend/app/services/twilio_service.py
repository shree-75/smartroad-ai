import os
import logging
import warnings
import certifi
import urllib3

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Suppress unverified HTTPS warnings for local dev SSL bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

USER_DEFAULT_PHONE = "+919704638232"

def format_phone_number(phone: str = None) -> str:
    """
    Formats phone numbers into standard E.164 international format (+919704638232).
    """
    if not phone:
        return os.getenv("EMERGENCY_PHONE_NUMBER") or USER_DEFAULT_PHONE
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    if len(phone) == 10 and phone.isdigit():
        return f"+91{phone}"
    if not phone.startswith("+"):
        return f"+{phone}"
    return phone

def get_twilio_client(account_sid: str, auth_token: str):
    """
    Returns a Twilio REST Client configured with SSL cafile fallback and SSL verification bypass if needed.
    """
    from twilio.rest import Client
    from twilio.http.http_client import TwilioHttpClient

    try:
        http_client = TwilioHttpClient()
        http_client.session.verify = False  # SSL fallback for local Windows environment
        return Client(account_sid, auth_token, http_client=http_client)
    except Exception:
        return Client(account_sid, auth_token)

def get_twilio_credentials():
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_PHONE_NUMBER")
    return sid, token, from_num

def send_emergency_sms(message_body: str, recipient_phone: str = None) -> dict:
    """
    Dispatches live emergency SMS notification using Twilio API to target number (+919704638232).
    """
    account_sid, auth_token, from_phone = get_twilio_credentials()
    to_phone = format_phone_number(recipient_phone)

    if not account_sid or not auth_token or not from_phone:
        logger.info(f"[Twilio SMS] Credentials missing in .env. Mock SMS to {to_phone}: {message_body}")
        return {
            "status": "MOCK_DISPATCHED",
            "to": to_phone,
            "message": f"Twilio credentials missing in .env file. Simulated SMS logged for {to_phone}.",
            "sms_body": message_body
        }

    try:
        client = get_twilio_client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_phone,
            to=to_phone
        )
        logger.info(f"[Twilio SMS] Live Emergency SMS sent! SID: {message.sid} to {to_phone}")
        return {
            "status": "SENT",
            "sid": message.sid,
            "to": to_phone,
            "from": from_phone,
            "message": f"Live Emergency SMS dispatched successfully to {to_phone}"
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
    Initiates a LIVE emergency phone call alert using Twilio Voice API to target number (+919704638232).
    Voice Script includes:
    1. Purpose Intro: "Hello! Urgent automated emergency safety call from SmartRoad AI."
    2. Why Calling (Reason): "We detected critical driver risk: {reason_text}."
    3. Suggestions: "Please pull over to a safe area on the shoulder immediately, park your vehicle, and take a rest break."
    """
    account_sid, auth_token, from_phone = get_twilio_credentials()
    target_phone = format_phone_number(to_phone)

    reason_text = alert_reason or "high risk driver status detected (mobile phone usage or fatigue)"

    # Structured TwiML Voice Script: Intro -> Why Calling -> Suggestion
    twiml_payload = (
        f'<Response>'
        f'<Say voice="alice">'
        f'Hello! This is an urgent automated emergency safety call from SmartRoad A I Driver Intelligence Network. '
        f'Purpose of call: We are calling because critical driver risk was detected on your vehicle monitor. '
        f'Detected hazard reason: {reason_text}. '
        f'Safety directive and suggestions for the driver: Please pull over to a safe location on the road shoulder immediately, park your vehicle, and take a rest break. Do not use your mobile phone while driving. Stay safe.'
        f'</Say>'
        f'</Response>'
    )

    if not account_sid or not auth_token or not from_phone:
        logger.info(f"[Twilio Voice] Credentials missing in .env. Mock Call to {target_phone} ({reason_text})")
        return {
            "status": "MOCK_CALL_INITIATED",
            "to": target_phone,
            "message": f"High Risk Twilio Call Triggered to {target_phone} (Simulated mode). Set TWILIO_ACCOUNT_SID in backend/.env.",
            "reason": reason_text
        }

    try:
        client = get_twilio_client(account_sid, auth_token)
        call = client.calls.create(
            twiml=twiml_payload,
            to=target_phone,
            from_=from_phone
        )
        logger.info(f"[Twilio Voice] LIVE Emergency Voice Call placed! SID: {call.sid} to {target_phone} from {from_phone}")
        return {
            "status": "CALL_INITIATED",
            "sid": call.sid,
            "to": target_phone,
            "from": from_phone,
            "message": f"LIVE Twilio voice call placed to {target_phone} from {from_phone}!",
            "reason": reason_text
        }
    except Exception as err:
        logger.error(f"[Twilio Voice Error] {err}")
        return {
            "status": "FAILED",
            "to": target_phone,
            "message": f"Twilio Voice Error: {str(err)}"
        }
