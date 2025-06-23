from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas.payment import CreatePayPalSessionRequest, PaymentOut
from app.services.paypal_service import create_checkout_session, PayPalService
from app.db.session import SessionLocal
from app.models.payment import Payment

router = APIRouter()
paypal_service = PayPalService()

@router.post("/checkout-session", response_model=PaymentOut)
async def create_paypal_checkout_session(payload: CreatePayPalSessionRequest):
    payment = await create_checkout_session(payload)
    print(payment)
    try:
        return payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/success")
async def paypal_success(paymentId: str, PayerID: str):
    db: Session = SessionLocal()

    try:
        payment = db.query(Payment).filter(Payment.payment_url.like(f"%{paymentId}%")).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        # Capture the order via your PayPalService method
        capture_result = await paypal_service.capture_order(paymentId)

        if capture_result.get("status") == "COMPLETED":
            payment.status = "completed"
            db.commit()
            return {"status": "Payment completed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Payment capture failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
