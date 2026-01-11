import pytest


class TestPersonalAccountsApi:
    @pytest.fixture
    def personal_account(self):
        return {"first_name": "John", "last_name": "Doe", "pesel": "12345678901"}

    @pytest.fixture
    def personal_account_2(self):
        return {"first_name": "Jim", "last_name": "Morris", "pesel": "09876543218"}

    def test_create_account(self, client, personal_account):
        response = client.post("/api/personal_accounts", json=personal_account)
        assert response.status_code == 201

    def test_create_duplicate_account(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        response = client.post("/api/personal_accounts", json=personal_account)
        assert response.status_code == 409
        assert response.get_json()["message"] == "Account with this PESEL already exists"

    def test_get_all_accounts(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        response = client.get("/api/personal_accounts")
        assert response.status_code == 200

    def test_get_count_accounts(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        response = client.get("/api/personal_accounts/count")
        assert response.status_code == 200
        assert response.get_json()['count'] == 1

    def test_get_account(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        response = client.get(f"/api/personal_accounts/{personal_account['pesel']}")
        assert response.status_code == 200

    def test_update_account(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        new_data = {"first_name": "James", "last_name": "Buck"}

        response = client.patch(f"/api/personal_accounts/{personal_account['pesel']}", json=new_data)
        assert response.status_code == 200
        assert response.get_json() == {"message": "Account updated"}

        get_response = client.get(f"/api/personal_accounts/{personal_account['pesel']}")
        updated_account = get_response.get_json()
        assert updated_account["first_name"] == "James"

    def test_delete_account(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        response = client.delete(f"/api/personal_accounts/{personal_account['pesel']}")
        assert response.status_code == 200

        get_response = client.get(f"/api/personal_accounts/{personal_account['pesel']}")
        assert get_response.status_code == 404


    def test_transfer_incoming(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        transfer_data = {"amount": 500, "type": "incoming"}

        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 200

        acc_response = client.get(f"/api/personal_accounts/{personal_account['pesel']}")
        assert acc_response.get_json()["balance"] == 500

    def test_transfer_outgoing_success(self, client, personal_account, personal_account_2):
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        client.post(f"/api/personal_accounts/{personal_account['pesel']}/transfer",
                    json={"amount": 1000, "type": "incoming"})

        transfer_data = {
            "amount": 200,
            "type": "outgoing",
            "receiver_pesel": personal_account_2["pesel"]
        }

        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 200
        assert response.get_json()["message"] == "Transfer in progress"

    def test_transfer_outgoing_insufficient_funds(self, client, personal_account, personal_account_2):
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {
            "amount": 10000,
            "type": "outgoing",
            "receiver_pesel": personal_account_2["pesel"]
        }

        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 422
        assert response.get_json()["error"] == "Insufficient funds"

    def test_transfer_invalid_type(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)

        transfer_data = {"amount": 100, "type": "crypto_scam"}
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 400

    def test_transfer_account_not_found(self, client):
        transfer_data = {"amount": 100, "type": "incoming"}
        response = client.post("/api/personal_accounts/99999999999/transfer", json=transfer_data)
        assert response.status_code == 404