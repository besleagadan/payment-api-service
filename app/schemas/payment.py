from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional
from datetime import datetime


class CreateStripeSessionRequest(BaseModel):
    product_name: str
    amount_usd: float
    success_url: HttpUrl
    cancel_url: HttpUrl


class CreateStripeSessionResponse(BaseModel):
    payment_id: UUID
    checkout_url: HttpUrl


class StripeWebhookEvent(BaseModel):
    session_id: str


class CreatePayPalSessionRequest(BaseModel):
    product_name: str
    amount_usd: float
    success_url: HttpUrl
    cancel_url: HttpUrl


class CreatePayPalSessionResponse(BaseModel):
    payment_id: str
    approval_url: HttpUrl

class PaymentOut(BaseModel):
    id: UUID
    provider: str
    product_name: str
    amount: float
    currency: str
    status: str
    payment_url: Optional[HttpUrl]
    created_at: datetime

    class Config:
        from_attributes = True


class CreateCryptoPaymentRequest(BaseModel):
    product_name: str
    amount_usd: float
    success_url: str
    cancel_url: str


class CreateCryptoPaymentResponse(BaseModel):
    payment_id: UUID
    payment_url: HttpUrl

