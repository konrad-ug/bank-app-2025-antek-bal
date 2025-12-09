import requests
import pytest

BASE_URL = "http://localhost:5000/api/personal_accounts"


class TestPersonalAccountsApi:
    @pytest.fixture
    def personal_account(self):
        pesel = "12345678901"
        data = {"first_name": "John", "last_name": "Doe", "pesel": pesel}
        yield data
        requests.delete(f"{BASE_URL}/{pesel}")

    @pytest.fixture
    def personal_account_2(self):
        pesel = "09876543218"
        data = {"first_name": "Jim", "last_name": "Morris", "pesel": pesel}
        yield data
        requests.delete(f"{BASE_URL}/{pesel}")

    def test_create_account(self, personal_account):
        response = requests.post(BASE_URL, json=personal_account)
        assert response.status_code == 201

    def test_get_all_accounts(self, personal_account):
        requests.post(BASE_URL, json=personal_account)
        response = requests.get(f"{BASE_URL}")
        assert response.status_code == 200

    def test_get_count_accounts(self, personal_account):
        requests.post(BASE_URL, json=personal_account)
        response = requests.get(f"{BASE_URL}/count")
        assert response.status_code == 200 and response.json()['count'] == 1

    def test_get_account(self, personal_account):
        requests.post(BASE_URL, json=personal_account)
        response = requests.get(f"{BASE_URL}/{personal_account['pesel']}")
        assert response.status_code == 200

    def test_update_account(self, personal_account):
        requests.post(BASE_URL, json=personal_account)
        new_data = {"first_name": "James", "last_name": "Buck"}

        response = requests.patch(f"{BASE_URL}/{personal_account['pesel']}", json=new_data)
        assert response.status_code == 200
        assert response.json() == {"message": "Account updated"}

        get_response = requests.get(f"{BASE_URL}/{personal_account['pesel']}")
        updated_account = get_response.json()

        assert updated_account["first_name"] == "James"
        assert updated_account["last_name"] == "Buck"
        assert updated_account["pesel"] == personal_account["pesel"]

    def test_delete_account(self, personal_account):
        requests.post(BASE_URL, json=personal_account)
        response = requests.delete(f"{BASE_URL}/{personal_account['pesel']}")

        assert response.status_code == 200
        assert response.json() == {"message": "Account deleted"}

        get_response = requests.get(f"{BASE_URL}/{personal_account['pesel']}")
        assert get_response.status_code == 404

    def test_outgoing_transfer(self, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        requests.post(BASE_URL, json=personal_account)
        requests.post(BASE_URL, json=personal_account_2)

        transfer_data = {
            "amount": 10,
            "receiver_pesel": personal_account_2["pesel"]
        }

        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/outgoing_transfer", json=transfer_data)

        assert response.status_code == 200
        assert response.json() == {"message": "Outgoing transfer successful"}

    def test_express_transfer(self, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        requests.post(BASE_URL, json=personal_account)
        requests.post(BASE_URL, json=personal_account_2)

        transfer_data = {
            "amount": 10,
            "receiver_pesel": personal_account_2["pesel"]
        }

        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/express_transfer", json=transfer_data)

        assert response.status_code == 200
        assert response.json() == {"message": "Express transfer successful"}

    def test_submit_for_loan(self, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        personal_account_2["promo_code"] = "PROM_123"

        requests.post(BASE_URL, json=personal_account)
        requests.post(BASE_URL, json=personal_account_2)

        transfer_data = {
            "amount": 10,
            "receiver_pesel": personal_account["pesel"]
        }

        for i in range(3):
            res = requests.post(f"{BASE_URL}/{personal_account_2['pesel']}/outgoing_transfer", json=transfer_data)
            assert res.status_code == 200

        loan_data = {"amount": 100}

        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/submit_for_loan", json=loan_data)

        assert response.status_code == 200
        assert response.json() == {"message": "Submission for loan successful"}

    def test_get_history_empty(self, personal_account):
        requests.post(BASE_URL, json=personal_account)

        response = requests.get(f"{BASE_URL}/{personal_account['pesel']}/history")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_history_after_transfer(self, personal_account, personal_account_2):
        personal_account["promo_code"] = "PROM_123"
        requests.post(BASE_URL, json=personal_account)
        requests.post(BASE_URL, json=personal_account_2)

        transfer_data = {
            "amount": 50,
            "receiver_pesel": personal_account_2["pesel"]
        }
        requests.post(f"{BASE_URL}/{personal_account['pesel']}/outgoing_transfer", json=transfer_data)

        response = requests.get(f"{BASE_URL}/{personal_account['pesel']}/history")

        assert response.status_code == 200
        history = response.json()

        assert len(history) == 1

        transaction = history[0]
        assert transaction["amount"] == -50
        assert transaction["type"] == "receiver"
        assert transaction["identity"] == personal_account_2["pesel"]

    def test_get_non_existent_account(self):
        response = requests.get(f"{BASE_URL}/99999999999")
        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}

    def test_update_non_existent_account(self):
        new_data = {"first_name": "Ghost"}
        response = requests.patch(f"{BASE_URL}/99999999999", json=new_data)
        assert response.status_code == 404

    def test_delete_non_existent_account(self):
        response = requests.delete(f"{BASE_URL}/99999999999")
        assert response.status_code == 404

    def test_transfer_failure_insufficient_funds(self, personal_account, personal_account_2):
        requests.post(BASE_URL, json=personal_account)
        requests.post(BASE_URL, json=personal_account_2)

        transfer_data = {
            "amount": 1000,
            "receiver_pesel": personal_account_2["pesel"]
        }

        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/outgoing_transfer", json=transfer_data)

        assert response.status_code == 400
        assert response.json() == {"error": "Outgoing transfer failed"}

    def test_transfer_failure_receiver_not_found(self, personal_account):
        personal_account["promo_code"] = "PROM_123"
        requests.post(BASE_URL, json=personal_account)

        transfer_data = {
            "amount": 10,
            "receiver_pesel": "00000000000"
        }

        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/outgoing_transfer", json=transfer_data)

        assert response.status_code == 404
        assert response.json() == {"error": "Sender or receiver account not found"}

    def test_loan_failure(self, personal_account):
        requests.post(BASE_URL, json=personal_account)

        loan_data = {"amount": 100}
        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/submit_for_loan", json=loan_data)

        assert response.status_code == 400
        assert response.json() == {"error": "Submission for loan failed"}

    def test_express_transfer_failure_insufficient_funds(self, personal_account, personal_account_2):
        requests.post(BASE_URL, json=personal_account)
        requests.post(BASE_URL, json=personal_account_2)

        transfer_data = {
            "amount": 1000,
            "receiver_pesel": personal_account_2["pesel"]
        }
        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/express_transfer", json=transfer_data)

        assert response.status_code == 400
        assert response.json() == {"error": "Express transfer failed"}

    def test_express_transfer_failure_receiver_not_found(self, personal_account):
        personal_account["promo_code"] = "PROM_123"
        requests.post(BASE_URL, json=personal_account)

        transfer_data = {
            "amount": 10,
            "receiver_pesel": "00000000000"
        }
        response = requests.post(f"{BASE_URL}/{personal_account['pesel']}/express_transfer", json=transfer_data)

        assert response.status_code == 404
        assert response.json() == {"error": "Sender or receiver account not found"}

    def test_loan_non_existent_account(self):
        loan_data = {"amount": 100}
        response = requests.post(f"{BASE_URL}/99999999999/submit_for_loan", json=loan_data)

        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}

    def test_history_non_existent_account(self):
        response = requests.get(f"{BASE_URL}/99999999999/history")

        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}