# Payment API Service

A modular, production-grade FastAPI service that supports payments through **Stripe**, **PayPal**, and **crypto (Coinbase Commerce)**.

Built for developers, startups, and payment SaaS platforms.

---

## Features

- Stripe Checkout + Webhooks
- PayPal REST API + payment execution
- Crypto payments via Coinbase Commerce
- Clean business logic layer (service-based)
- Modular FastAPI structure
- PostgreSQL via SQLAlchemy
- Dockerized for local development
- Ready for testing (Pytest structure included)
- `.env`-based secret management
- Easy to extend for future providers (Binance, Paynet, etc.)

---

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **Docker + Docker Compose**
- **SQLAlchemy**
- **Pydantic**
- **Stripe SDK**
- **PayPal REST SDK**
- **Coinbase Commerce SDK**

---

## 🚧 API Overview

| Method | Endpoint                                 | Description                        |
|--------|------------------------------------------|------------------------------------|
| POST   | `/api/v1/stripe/checkout-session`        | Create Stripe checkout session     |
| POST   | `/api/v1/stripe/webhook`                 | Stripe webhook handler             |
| POST   | `/api/v1/paypal/checkout-session`        | Create PayPal payment              |
| GET    | `/api/v1/paypal/success`                 | PayPal payment success confirm     |
| POST   | `/api/v1/crypto/checkout-session`        | Create crypto payment (Coinbase)   |
| POST   | `/api/v1/crypto/webhook`                 | Coinbase webhook handler           |
| GET    | `/health`                                | Healthcheck route                  |

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/payment-api-service.git
cd payment-api-service
```

---

## Create .env file

```bash
# PostgreSQL Database
POSTGRES_DB=payment_servide
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Stripe
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...

# PayPal
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_ENV=sandbox

# Coinbase
COINBASE_COMMERCE_API_KEY=...
COINBASE_WEBHOOK_SECRET=...
```

---

## Run Docker

```bash
docker-compose up --build
docker-compose down
docker-compose exec web bash
```

---

## Running Tests

```bash
docker-compose exec web bash
pytest
```

---

## Project Structure

```pgsql
app/
├── api/v1/routes/         → API endpoints (stripe, paypal, crypto)
├── core/                  → Config & environment
├── services/              → Business logic
├── schemas/               → Pydantic models
├── models/                → SQLAlchemy models
├── db/                    → DB session and base
└── main.py                → FastAPI app entry
```

---

## What We Built (Development Steps)

### Phase 1 – Project Setup & Structure

- Initialized FastAPI project with modular app structure
- Added `.env` for managing secrets
- Created base route: `/health`
- Added Docker support with `Dockerfile` and `docker-compose.yml`
- Installed FastAPI, Uvicorn, and dotenv

### Phase 2 – Stripe Integration

- Added dynamic Stripe Checkout creation
- sed Pydantic to validate request and response
- Created `Payment` model to store each payment record
- Linked `payment_id` with Stripe metadata
- Saved payment to PostgreSQL with status and session_id
- Structured code to easily extend to other payment providers

### Phase 3 – PayPal Integration

- Installed PayPal REST SDK and connected with sandbox credentials
- Created service to generate PayPal payment links
- Created `/api/v1/paypal/checkout-session` to generate approval URLs
- Stored PayPal payment info into shared `Payment` model
- Used Pydantic for strong request/response validation

### Phase X – Payment Webhook Handling

- Added Stripe webhook at `/api/v1/stripe/webhook` to update payment status on events
- Implemented PayPal payment confirmation via`/api/v1/paypal/success` endpoint
- Updated payment records in DB to reflect real-time status
- Ensured error handling and logging for webhook processing

### Phase 4 – Crypto Payments Integration

- Integrated Coinbase Commerce for crypto payments
- Created API to generate crypto payment charges with product info
- Saved crypto payments in unified Payment model
- Added webhook support to confirm payment status updates
- Extended API router with `/api/v1/crypto` prefix

---

## Resources & Inspiration

- [Stripe API Docs](https://docs.stripe.com/api)
- [PayPal Developer Docs](https://developer.paypal.com/docs/api/overview/)
- [Coinbase Commerce API](https://commerce.coinbase.com/docs/api/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [RealWorld FastAPI App](https://github.com/nsidnev/fastapi-realworld-example-app)
- [tiangolo/full-stack-fastapi-postgresql](https://github.com/fastapi/full-stack-fastapi-template)
