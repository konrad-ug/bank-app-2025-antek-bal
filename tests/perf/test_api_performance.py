import pytest, time
from app.api import app


class TestPerformance:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def personal_account(self):
        return {"first_name": "John", "last_name": "Doe", "pesel": "12345678901"}

    def test_account_creation_performance(self, personal_account, client):
        for _ in range(100):
            start_creat = time.perf_counter()
            response_creat = client.post("/api/personal_accounts", json=personal_account)
            end_creat = time.perf_counter()

            assert response_creat.status_code == 201

            duration_creat = end_creat - start_creat
            assert duration_creat < 0.5

            start_del = time.perf_counter()
            response_del = client.delete(f"/api/personal_accounts/{personal_account['pesel']}", json=personal_account)
            end_del = time.perf_counter()

            assert response_del.status_code == 200

            duration_del = end_del - start_del
            assert duration_del < 0.5

    def test_transfers_performance(self, personal_account, client):
        client.post("/api/personal_accounts", json=personal_account)

        transfer = {"type": "incoming", "amount": 50}

        for _ in range(100):
            start_transfer = time.perf_counter()
            response = client.post(f"/api/personal_accounts/{personal_account['pesel']}/transfer", json=transfer)
            end_transfer = time.perf_counter()

            assert response.status_code == 200

            duration = end_transfer - start_transfer
            assert duration < 0.5

        response_get = client.get(f"/api/personal_accounts/{personal_account['pesel']}")
        assert response_get.status_code == 200

        balance = response_get.get_json()["balance"]
        assert balance == 100 * transfer['amount']
