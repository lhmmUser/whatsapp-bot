from fastapi import Request, FastAPI
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from app.gemini import get_gemini_response

app = FastAPI()
@app.post("/twilio-webhook")
async def twilio_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body")
    sender = form.get("From")

    print(f"Message from {sender}: {incoming_msg}")

    reply_text = await get_gemini_response(incoming_msg)

    resp = MessagingResponse()
    resp.message(reply_text)
    return PlainTextResponse(str(resp), media_type="application/xml")
