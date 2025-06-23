def test_stripe_checkout(client, monkeypatch):
    def mock_create_checkout_session(data):
        class MockPayment:
            id = "fake-stripe-id"
            payment_url = "https://stripe.com/test_checkout"
        return MockPayment()

    from app.services import stripe_service
    monkeypatch.setattr(stripe_service, "create_checkout_session", mock_create_checkout_session)

    payload = {
        "product_name": "Test Product",
        "amount_usd": 10.5,
        "success_url": "https://test.com/success",
        "cancel_url": "https://test.com/cancel"
    }

    response = client.post("/api/v1/stripe/checkout-session", json=payload)
    assert response.status_code == 200
    assert "checkout_url" in response.json()
