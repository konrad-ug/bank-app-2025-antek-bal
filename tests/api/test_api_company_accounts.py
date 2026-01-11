import pytest
from app.api import account_registry


class TestCompanyAccountsApi:
    @pytest.fixture
    def company_account(self):
        return {"company_name": "Test Corp", "nip": "1234567890"}

    @pytest.fixture
    def company_account_2(self):
        return {"company_name": "Second Corp", "nip": "0987654321"}

    @pytest.fixture
    def fund_provider(self, client):
        data = {"first_name": "Rich", "last_name": "Person", "pesel": "12345678901", "promo_code": "PROM_123"}
        client.post("/api/personal_accounts", json=data)
        client.post(f"/api/personal_accounts/{data['pesel']}/transfer",
                    json={"amount": 10000, "type": "incoming"})
        return data

    def test_create_account(self, client, company_account):
        response = client.post("/api/company_accounts", json=company_account)
        assert response.status_code == 201

    def test_create_duplicate_account(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)
        response = client.post("/api/company_accounts", json=company_account)
        assert response.status_code == 409
        assert response.get_json()["message"] == "Account with this NIP already exists"

    def test_get_all_accounts(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)
        response = client.get("/api/company_accounts")
        assert response.status_code == 200
        assert len(response.get_json()) == 1

    def test_get_count_accounts(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)
        response = client.get("/api/company_accounts/count")
        assert response.status_code == 200
        assert response.get_json()['count'] == 1

    def test_get_account(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)
        response = client.get(f"/api/company_accounts/{company_account['nip']}")
        assert response.status_code == 200

    def test_update_account(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)
        response = client.patch(f"/api/company_accounts/{company_account['nip']}",
                                json={"company_name": "Updated Corp"})
        assert response.status_code == 200

    def test_delete_account(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)
        response = client.delete(f"/api/company_accounts/{company_account['nip']}")
        assert response.status_code == 200

    def test_transfers_unified_endpoint(self, client, company_account, company_account_2, fund_provider):
        client.post("/api/company_accounts", json=company_account)
        client.post("/api/company_accounts", json=company_account_2)

        client.post(f"/api/personal_accounts/{fund_provider['pesel']}/transfer",
                    json={"amount": 200, "type": "outgoing", "receiver_nip": company_account["nip"]})

        client.post(f"/api/company_accounts/{company_account['nip']}/transfer",
                    json={"amount": 50, "type": "outgoing", "receiver_nip": company_account_2["nip"]})

        client.post(f"/api/company_accounts/{company_account['nip']}/transfer",
                    json={"amount": 10, "type": "express", "receiver_nip": company_account_2["nip"]})

        response = client.get(f"/api/company_accounts/{company_account['nip']}/history")
        assert response.status_code == 200
        history = response.get_json()
        assert len(history) == 4

    def test_successful_loan(self, client, company_account, fund_provider):
        client.post("/api/company_accounts", json=company_account)

        client.post(f"/api/personal_accounts/{fund_provider['pesel']}/transfer",
                    json={"amount": 5000, "type": "outgoing", "receiver_nip": company_account["nip"]})

        zus = {"company_name": "ZUS", "nip": "6666666666"}
        client.post("/api/company_accounts", json=zus)

        client.post(f"/api/company_accounts/{company_account['nip']}/transfer",
                    json={"amount": 1775, "type": "outgoing", "receiver_nip": zus["nip"]})

        response = client.post(f"/api/company_accounts/{company_account['nip']}/submit_for_loan", json={"amount": 1000})
        assert response.status_code == 200

    def test_outgoing_transfer_failures(self, client, company_account):
        client.post("/api/company_accounts", json=company_account)

        res1 = client.post(f"/api/company_accounts/{company_account['nip']}/transfer",
                           json={"amount": 1000, "type": "outgoing", "receiver_nip": "1234567890"})
        assert res1.status_code == 422

        res2 = client.post(f"/api/company_accounts/{company_account['nip']}/transfer",
                           json={"amount": 10, "type": "outgoing", "receiver_nip": "0000000000"})
        assert res2.status_code == 404

        res3 = client.post(f"/api/company_accounts/{company_account['nip']}/transfer",
                           json={"amount": 10, "type": "scam", "receiver_nip": "1234567890"})
        assert res3.status_code == 400

    def test_get_non_existent(self, client):
        response = client.get("/api/company_accounts/0000000000")
        assert response.status_code == 404

    def test_update_non_existent(self, client):
        response = client.patch("/api/company_accounts/0000000000", json={"company_name": "Ghost"})
        assert response.status_code == 404

    def test_delete_non_existent(self, client):
        response = client.delete("/api/company_accounts/0000000000")
        assert response.status_code == 404