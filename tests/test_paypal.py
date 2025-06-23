def test_paypal_checkout(client, monkeypatch):
    def mock_create_paypal_payment(data):
        class MockPayment:
            id = "fake-paypal-id"
            payment_url = "https://paypal.com/checkout"
        return MockPayment()

    from app.services import paypal_service
    monkeypatch.setattr(paypal_service, "create_paypal_payment", mock_create_paypal_payment)

    payload = {
        "product_name": "YouTube Premium",
        "amount_usd": 9.99,
        "success_url": "https://test.com/success",
        "cancel_url": "https://test.com/cancel"
    }

    response = client.post("/api/v1/paypal/checkout-session", json=payload)
    assert response.status_code == 200
    assert "approval_url" in response.json()
