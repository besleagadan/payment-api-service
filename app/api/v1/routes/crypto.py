from fastapi import APIRouter, HTTPException, Request
from coinbase_commerce.webhook import Webhook
from app.core.config import settings
from app.schemas.payment import CreateCryptoPaymentRequest, CreateCryptoPaymentResponse
from app.services.crypto_service import create_coinbase_charge
from app.db.session import SessionLocal
from app.models.payment import Payment

router = APIRouter()

@router.post("/checkout-session", response_model=CreateCryptoPaymentResponse)
def create_crypto_payment(payload: CreateCryptoPaymentRequest):
    try:
        payment = create_coinbase_charge(payload)
        return {
            "payment_id": payment.id,
            "payment_url": payment.payment_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def coinbase_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-CC-Webhook-Signature")

    try:
        event = Webhook.construct_event(payload, signature, settings.COINBASE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook verification failed: {str(e)}")

    db = SessionLocal()

    payment_id = event.data.get("metadata", {}).get("payment_id")
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment:
        if event.type == "charge:confirmed":
            payment.status = "completed"
        elif event.type == "charge:failed":
            payment.status = "failed"
        db.commit()

    db.close()
    return {"status": "success"}
