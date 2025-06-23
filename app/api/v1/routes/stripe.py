import stripe
from fastapi import APIRouter, HTTPException, Request
from app.core.config import settings
from app.schemas.payment import CreateStripeSessionRequest, CreateStripeSessionResponse
from app.services.stripe_service import create_checkout_session
from app.db.session import SessionLocal
from app.models.payment import Payment


router = APIRouter()

@router.post("/checkout-session", response_model=CreateStripeSessionResponse)
def create_checkout_session_endpoint(payload: CreateStripeSessionRequest):
    try:
        payment = create_checkout_session(payload)
        return {
            "payment_id": payment.id,
            "checkout_url": payment.payment_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    db = SessionLocal()

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment_id = session.get("metadata", {}).get("payment_id")
        if payment_id:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if payment:
                payment.status = "completed"
                db.commit()

    db.close()
    return {"status": "success"}
