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

    def test_outgoing_transfer(self, client, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {"amount": 10, "receiver_pesel": personal_account_2["pesel"]}
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/outgoing_transfer",
                               json=transfer_data)

        assert response.status_code == 200
        assert response.get_json() == {"message": "Outgoing transfer successful"}

    def test_express_transfer(self, client, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {"amount": 10, "receiver_pesel": personal_account_2["pesel"]}
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/express_transfer",
                               json=transfer_data)

        assert response.status_code == 200

    def test_submit_for_loan(self, client, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        personal_account_2["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {"amount": 10, "receiver_pesel": personal_account["pesel"]}
        for _ in range(3):
            client.post(f"/api/personal_accounts/{personal_account_2['pesel']}/outgoing_transfer", json=transfer_data)

        loan_data = {"amount": 100}
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/submit_for_loan", json=loan_data)

        assert response.status_code == 200
        assert response.get_json() == {"message": "Submission for loan successful"}

    def test_get_history(self, client, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {"amount": 50, "receiver_pesel": personal_account_2["pesel"]}
        client.post(f"/api/personal_accounts/{personal_account['pesel']}/outgoing_transfer", json=transfer_data)

        response = client.get(f"/api/personal_accounts/{personal_account['pesel']}/history")
        assert response.status_code == 200
        assert len(response.get_json()) == 1

    def test_history_with_express_transfer(self, client, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        client.post(f"/api/personal_accounts/{personal_account['pesel']}/express_transfer",
                    json={"amount": 10, "receiver_pesel": personal_account_2["pesel"]})

        response = client.get(f"/api/personal_accounts/{personal_account['pesel']}/history")
        assert response.status_code == 200
        history = response.get_json()

        charge = next((item for item in history if item["type"] == "charge"), None)
        assert charge is not None
        assert charge["identity"] == "express transfer"

    def test_history_transfer_to_company(self, client, personal_account):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)

        company_data = {"company_name": "Test Corp", "nip": "1234567890"}
        client.post("/api/company_accounts", json=company_data)

        client.post(f"/api/personal_accounts/{personal_account['pesel']}/outgoing_transfer",
                    json={"amount": 10, "receiver_nip": company_data["nip"]})

        response = client.get(f"/api/personal_accounts/{personal_account['pesel']}/history")
        assert response.status_code == 200
        history = response.get_json()

        assert history[-1]["identity"] == company_data["nip"]

    def test_get_non_existent_account(self, client):
        response = client.get("/api/personal_accounts/99999999999")
        assert response.status_code == 404

    def test_update_non_existent_account(self, client):
        response = client.patch("/api/personal_accounts/99999999999", json={"first_name": "Ghost"})
        assert response.status_code == 404

    def test_delete_non_existent_account(self, client):
        response = client.delete("/api/personal_accounts/99999999999")
        assert response.status_code == 404

    def test_transfer_failure_insufficient_funds(self, client, personal_account, personal_account_2):
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {"amount": 1000, "receiver_pesel": personal_account_2["pesel"]}
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/outgoing_transfer",
                               json=transfer_data)
        assert response.status_code == 400

    def test_transfer_failure_receiver_not_found(self, client, personal_account):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/outgoing_transfer",
                               json={"amount": 10, "receiver_pesel": "00000000000"})
        assert response.status_code == 404

    def test_express_transfer_failure_receiver_not_found(self, client, personal_account):
        personal_account["promo_code"] = "PROM_123"
        client.post("/api/personal_accounts", json=personal_account)
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/express_transfer",
                               json={"amount": 10, "receiver_pesel": "00000000000"})
        assert response.status_code == 404

    def test_loan_failure(self, client, personal_account):
        client.post("/api/personal_accounts", json=personal_account)
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/submit_for_loan",
                               json={"amount": 100})
        assert response.status_code == 400

    def test_history_non_existent_account(self, client):
        response = client.get("/api/personal_accounts/99999999999/history")
        assert response.status_code == 404

    def test_express_transfer_failure_insufficient_funds(self, client, personal_account, personal_account_2):
        client.post("/api/personal_accounts", json=personal_account)
        client.post("/api/personal_accounts", json=personal_account_2)

        transfer_data = {"amount": 1000, "receiver_pesel": personal_account_2["pesel"]}
        response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/express_transfer",
                               json=transfer_data)

        assert response.status_code == 400
        assert response.get_json() == {"error": "Express transfer failed"}

    def test_loan_non_existent_account(self, client):
        loan_data = {"amount": 100}
        response = client.post("/api/personal_accounts/99999999999/submit_for_loan", json=loan_data)

        assert response.status_code == 404
        assert response.get_json() == {"error": "Account not found"}