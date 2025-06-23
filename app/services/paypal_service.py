from uuid import uuid4
import httpx
from typing import Optional
from dataclasses import dataclass

from app.core.config import settings
from app.core.logger import logger
from app.models.payment import Payment
from app.db.session import SessionLocal


# @dataclass
# class PayPalOrder:
#     id: str
#     approval_url: str


class PaymentCreationError(Exception):
    def __init__(self, provider: str, message: str):
        self.provider = provider
        self.message = message
        super().__init__(f"[{provider}] {message}")

class PayPalService:
    def __init__(self):
        self.base_url = (
            "https://api-m.sandbox.paypal.com"
            if settings.PAYPAL_ENV == "sandbox"
            else "https://api-m.paypal.com"
        )
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET

    async def get_access_token(self) -> str:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/v1/oauth2/token",
                    auth=(self.client_id, self.client_secret),
                    data={"grant_type": "client_credentials"},
                    headers={"Accept": "application/json"},
                    timeout=10,
                )
                resp.raise_for_status()
                return resp.json()["access_token"]
            except httpx.HTTPError as e:
                logger.error(f"PayPal token error: {e}")
                raise PaymentCreationError("paypal", "Failed to get access token")

    async def create_order(self, access_token: str, product_name: str, amount_usd: float,
                           success_url: str, cancel_url: str, currency: str = "USD") -> dict:
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": f"{amount_usd:.2f}"
                },
                "description": product_name
            }],
            "application_context": {
                "return_url": str(success_url),
                "cancel_url": str(cancel_url)
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/v2/checkout/orders",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {access_token}"
                    },
                    timeout=10,
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as e:
                logger.error(f"PayPal order creation error: {e}")
                raise PaymentCreationError("paypal", "Failed to create PayPal order")

    async def capture_order(self, order_id: str) -> dict:
        access_token = await self.get_paypal_access_token()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.get_paypal_base_url()}/v2/checkout/orders/{order_id}/capture",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
            )
            response.raise_for_status()
            return response.json()

async def create_checkout_session(data):
    paypal_service = PayPalService()

    access_token = await paypal_service.get_access_token()
    order_data = await paypal_service.create_order(
        access_token,
        product_name=data.product_name,
        amount_usd=data.amount_usd,
        success_url=data.success_url,
        cancel_url=data.cancel_url,
    )

    approval_url = next(
        (link["href"] for link in order_data["links"] if link["rel"] == "approve"),
        None
    )
    if not approval_url:
        raise Exception("Approval URL not found")

    db = SessionLocal()
    try:
        payment = Payment(
            id=uuid4(),
            provider="paypal",
            product_name=data.product_name,
            amount=data.amount_usd,
            currency="USD",
            status="pending",
            session_id=order_data["id"],
            payment_url=approval_url,
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
    finally:
        db.close()
