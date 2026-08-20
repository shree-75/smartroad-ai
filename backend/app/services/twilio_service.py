import os

def send_emergency_sms(message_body, recipient_phone=None):
    """
    Dispatches emergency SMS notification using Twilio API.
    Reads credentials strictly from environment variables.
    Returns status dict without crashing if Twilio is not configured.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    to_phone = recipient_phone or os.getenv("EMERGENCY_PHONE_NUMBER")

    if not account_sid or not auth_token or not from_phone or not to_phone:
        return {
            "status": "NOT_CONFIGURED",
            "message": "TWILIO: NOT CONFIGURED (Environment credentials missing)"
        }

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_phone,
            to=to_phone
        )
        return {
            "status": "SENT",
            "sid": message.sid,
            "message": "Emergency SMS dispatched successfully"
        }
    except Exception as err:
        return {
            "status": "FAILED",
            "message": f"Twilio SMS Error: {str(err)}"
        }

def make_emergency_call(to_phone=None):
    """
    Initiates an emergency phone call alert using Twilio Voice API.
    Returns status dict without crashing if credentials are missing.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    target_phone = to_phone or os.getenv("EMERGENCY_PHONE_NUMBER")

    if not account_sid or not auth_token or not from_phone or not target_phone:
        return {
            "status": "NOT_CONFIGURED",
            "message": "TWILIO VOICE: NOT CONFIGURED (Environment credentials missing)"
        }

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            twiml='<Response><Say voice="alice">Critical Driver Alert! SmartRoad AI has detected severe driver drowsiness or critical risk. Immediate assistance required.</Say></Response>',
            to=target_phone,
            from_=from_phone
        )
        return {
            "status": "CALL_INITIATED",
            "sid": call.sid,
            "message": "Emergency voice call initiated successfully"
        }
    except Exception as err:
        return {
            "status": "FAILED",
            "message": f"Twilio Voice Error: {str(err)}"
        }
