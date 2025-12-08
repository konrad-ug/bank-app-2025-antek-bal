import requests
import pytest

BASE_URL = "http://localhost:3000/api/personal_accounts"

class TestPersonalAccountsApi:
    
    @pytest.fixture
    def created_account(self):
        """
        Ta fixtura:
        1. Tworzy dane
        2. Czyści serwer po teście (TEARDOWN)
        """
        pesel = "12345678901"
        data = {"first_name": "Jan", "last_name": "Kowalski", "pesel": pesel}
        
        yield data
        
        requests.delete(f"{BASE_URL}/{pesel}")

    def test_create_account(self, created_account):
        response = requests.post(BASE_URL, json=created_account)
        assert response.status_code == 201

    def test_get_account(self, created_account):
        requests.post(BASE_URL, json=created_account)
        
        response = requests.get(f"{BASE_URL}/{created_account['pesel']}")
        assert response.status_code == 200