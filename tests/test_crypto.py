def test_crypto_checkout(client, monkeypatch):
    def mock_create_coinbase_charge(data):
        class MockPayment:
            id = "fake-crypto-id"
            payment_url = "https://commerce.coinbase.com/charge/123"
        return MockPayment()

    from app.services import crypto_service
    monkeypatch.setattr(crypto_service, "create_coinbase_charge", mock_create_coinbase_charge)

    payload = {
        "product_name": "Crypto Item",
        "amount_usd": 5.25,
        "success_url": "https://test.com/success",
        "cancel_url": "https://test.com/cancel"
    }

    response = client.post("/api/v1/crypto/checkout-session", json=payload)
    assert response.status_code == 200
    assert "payment_url" in response.json()
