import stripe
from uuid import uuid4
from app.core.config import settings
from app.models.payment import Payment
from app.db.session import SessionLocal

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(data):
    db = SessionLocal()

    payment_id = uuid4()

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": data.product_name,
                    },
                    "unit_amount": int(data.amount_usd * 100),  # cents
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=data.success_url,
        cancel_url=data.cancel_url,
        metadata={"payment_id": str(payment_id)}
    )

    payment = Payment(
        id=payment_id,
        product_name=data.product_name,
        amount=data.amount_usd,
        status="pending",
        session_id=session.id,
        payment_url=session.url
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    db.close()

    return payment
