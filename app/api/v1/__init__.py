from fastapi import APIRouter
from .routes import (
    stripe,
    paypal,
    crypto
)

api_router = APIRouter()
api_router.include_router(stripe.router, prefix="/stripe", tags=["Stripe"])
api_router.include_router(paypal.router, prefix="/paypal", tags=["PayPal"])
api_router.include_router(crypto.router, prefix="/crypto", tags=["Crypto"])
