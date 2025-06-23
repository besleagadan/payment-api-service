from coinbase_commerce.client import Client
from uuid import uuid4
from app.db.session import SessionLocal
from app.models.payment import Payment
from app.core.config import settings

client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)

def create_coinbase_charge(data):
    db = SessionLocal()
    payment_id = uuid4()

    charge_data = {
        "name": data.product_name,
        "description": f"Payment for {data.product_name}",
        "local_price": {
            "amount": f"{data.amount_usd:.2f}",
            "currency": "USD"
        },
        "pricing_type": "fixed_price",
        "metadata": {
            "payment_id": str(payment_id)
        },
        "redirect_url": data.success_url,
        "cancel_url": data.cancel_url
    }

    charge = client.charge.create(**charge_data)

    print("___ START")
    print(charge)

    payment = Payment(
        id=payment_id,
        provider="coinbase_commerce",
        product_name=data.product_name,
        amount=data.amount_usd,
        currency="USD",
        status="pending",
        payment_url=charge.hosted_url
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)
    db.close()

    return payment
