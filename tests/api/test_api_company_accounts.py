import requests
import pytest

BASE_URL = "http://localhost:5000/api/company_accounts"
PERSONAL_URL = "http://localhost:5000/api/personal_accounts"


class TestCompanyAccountsApi:
    @pytest.fixture
    def company_account(self):
        nip = "1234567890"
        data = {"company_name": "Test Corp", "nip": nip}
        yield data
        requests.delete(f"{BASE_URL}/{nip}")

    @pytest.fixture
    def company_account_2(self):
        nip = "0987654321"
        data = {"company_name": "Second Corp", "nip": nip}
        yield data
        requests.delete(f"{BASE_URL}/{nip}")

    @pytest.fixture
    def fund_provider(self):
        pesel = "12345678901"
        data = {"first_name": "Rich", "last_name": "Person", "pesel": pesel, "promo_code": "PROM_123"}
        requests.post(PERSONAL_URL, json=data)
        yield data
        requests.delete(f"{PERSONAL_URL}/{pesel}")

    def test_create_account(self, company_account):
        response = requests.post(BASE_URL, json=company_account)
        assert response.status_code == 201

    def test_get_all_accounts(self, company_account):
        requests.post(BASE_URL, json=company_account)
        response = requests.get(BASE_URL)
        assert response.status_code == 200

    def test_get_count_accounts(self, company_account):
        requests.post(BASE_URL, json=company_account)
        response = requests.get(f"{BASE_URL}/count")
        assert response.status_code == 200 and response.json()['count'] == 1

    def test_get_account(self, company_account):
        requests.post(BASE_URL, json=company_account)
        response = requests.get(f"{BASE_URL}/{company_account['nip']}")
        assert response.status_code == 200

    def test_update_account(self, company_account):
        requests.post(BASE_URL, json=company_account)
        new_data = {"company_name": "Updated Corp"}

        response = requests.patch(f"{BASE_URL}/{company_account['nip']}", json=new_data)
        assert response.status_code == 200
        assert response.json() == {"message": "Account updated"}

        get_response = requests.get(f"{BASE_URL}/{company_account['nip']}")
        updated_account = get_response.json()

        assert updated_account["company_name"] == "Updated Corp"
        assert updated_account["nip"] == company_account["nip"]

    def test_delete_account(self, company_account):
        requests.post(BASE_URL, json=company_account)
        response = requests.delete(f"{BASE_URL}/{company_account['nip']}")

        assert response.status_code == 200
        assert response.json() == {"message": "Account deleted"}

        get_response = requests.get(f"{BASE_URL}/{company_account['nip']}")
        assert get_response.status_code == 404

    def test_outgoing_transfer(self, company_account, company_account_2, fund_provider):
        requests.post(BASE_URL, json=company_account)
        requests.post(BASE_URL, json=company_account_2)

        funding_transfer = {
            "amount": 50,
            "receiver_nip": company_account["nip"]
        }
        requests.post(f"{PERSONAL_URL}/{fund_provider['pesel']}/outgoing_transfer", json=funding_transfer)

        transfer_data = {
            "amount": 10,
            "receiver_nip": company_account_2["nip"]
        }

        response = requests.post(f"{BASE_URL}/{company_account['nip']}/outgoing_transfer", json=transfer_data)

        assert response.status_code == 200
        assert response.json() == {"message": "Outgoing transfer successful"}

    def test_express_transfer(self, company_account, company_account_2, fund_provider):
        requests.post(BASE_URL, json=company_account)
        requests.post(BASE_URL, json=company_account_2)

        funding_transfer = {
            "amount": 50,
            "receiver_nip": company_account["nip"]
        }
        requests.post(f"{PERSONAL_URL}/{fund_provider['pesel']}/outgoing_transfer", json=funding_transfer)

        transfer_data = {
            "amount": 10,
            "receiver_nip": company_account_2["nip"]
        }

        response = requests.post(f"{BASE_URL}/{company_account['nip']}/express_transfer", json=transfer_data)

        assert response.status_code == 200
        assert response.json() == {"message": "Express transfer successful"}

    def test_get_history_after_transfer(self, company_account, company_account_2, fund_provider):
        requests.post(BASE_URL, json=company_account)
        requests.post(BASE_URL, json=company_account_2)

        funding_transfer = {
            "amount": 50,
            "receiver_nip": company_account["nip"]
        }
        requests.post(f"{PERSONAL_URL}/{fund_provider['pesel']}/outgoing_transfer", json=funding_transfer)

        transfer_data = {
            "amount": 50,
            "receiver_nip": company_account_2["nip"]
        }
        requests.post(f"{BASE_URL}/{company_account['nip']}/outgoing_transfer", json=transfer_data)

        response = requests.get(f"{BASE_URL}/{company_account['nip']}/history")

        assert response.status_code == 200
        history = response.json()

        assert len(history) == 2

        outgoing_transaction = history[1]
        assert outgoing_transaction["amount"] == -50
        assert outgoing_transaction["identity"] == company_account_2["nip"]

    def test_get_non_existent_account(self):
        response = requests.get(f"{BASE_URL}/0000000000")
        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}

    def test_update_non_existent_account(self):
        new_data = {"company_name": "Ghost Corp"}
        response = requests.patch(f"{BASE_URL}/0000000000", json=new_data)
        assert response.status_code == 404

    def test_delete_non_existent_account(self):
        response = requests.delete(f"{BASE_URL}/0000000000")
        assert response.status_code == 404

    def test_transfer_failure_insufficient_funds(self, company_account, company_account_2):
        requests.post(BASE_URL, json=company_account)
        requests.post(BASE_URL, json=company_account_2)

        transfer_data = {
            "amount": 1000,
            "receiver_nip": company_account_2["nip"]
        }

        response = requests.post(f"{BASE_URL}/{company_account['nip']}/outgoing_transfer", json=transfer_data)

        assert response.status_code == 400
        assert response.json() == {"error": "Outgoing transfer failed"}

    def test_transfer_failure_receiver_not_found(self, company_account, fund_provider):
        requests.post(BASE_URL, json=company_account)

        funding_transfer = {
            "amount": 100,
            "receiver_nip": company_account["nip"]
        }
        requests.post(f"{PERSONAL_URL}/{fund_provider['pesel']}/outgoing_transfer", json=funding_transfer)

        transfer_data = {
            "amount": 10,
            "receiver_nip": "0000000000"
        }

        response = requests.post(f"{BASE_URL}/{company_account['nip']}/outgoing_transfer", json=transfer_data)

        assert response.status_code == 404
        assert response.json() == {"error": "Sender or receiver account not found"}

    def test_express_transfer_failure_insufficient_funds(self, company_account, company_account_2):
        requests.post(BASE_URL, json=company_account)
        requests.post(BASE_URL, json=company_account_2)

        transfer_data = {
            "amount": 1000,
            "receiver_nip": company_account_2["nip"]
        }

        response = requests.post(f"{BASE_URL}/{company_account['nip']}/express_transfer", json=transfer_data)

        assert response.status_code == 400
        assert response.json() == {"error": "Express transfer failed"}

    def test_express_transfer_failure_receiver_not_found(self, company_account, fund_provider):
        requests.post(BASE_URL, json=company_account)

        funding_transfer = {
            "amount": 100,
            "receiver_nip": company_account["nip"]
        }
        requests.post(f"{PERSONAL_URL}/{fund_provider['pesel']}/outgoing_transfer", json=funding_transfer)

        transfer_data = {
            "amount": 10,
            "receiver_nip": "0000000000"
        }
        response = requests.post(f"{BASE_URL}/{company_account['nip']}/express_transfer", json=transfer_data)

        assert response.status_code == 404
        assert response.json() == {"error": "Sender or receiver account not found"}

    def test_loan_failure(self, company_account):
        requests.post(BASE_URL, json=company_account)

        loan_data = {"amount": 10000}
        response = requests.post(f"{BASE_URL}/{company_account['nip']}/submit_for_loan", json=loan_data)

        assert response.status_code == 400
        assert response.json() == {"error": "Submission for loan failed"}

    def test_loan_non_existent_account(self):
        loan_data = {"amount": 100}
        response = requests.post(f"{BASE_URL}/0000000000/submit_for_loan", json=loan_data)

        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}

    def test_history_non_existent_account(self):
        response = requests.get(f"{BASE_URL}/0000000000/history")

        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}
