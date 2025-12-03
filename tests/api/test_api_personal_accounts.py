from app.api import account_registry

class TestPersonalAccountsApi:
    
    def test_create_account(self, client):
        data = {"first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901"}
        response = client.post("/api/personal_accounts", json=data)
        
        assert response.status_code == 201
        assert len(account_registry.personal_accounts) == 1

    def test_get_account_by_pesel(self, client):
        data = {"first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901"}
        client.post("/api/personal_accounts", json=data)

        response = client.get("/api/personal_accounts/12345678901")
        assert response.status_code == 200
        assert response.get_json()["first_name"] == "Jan"

    def test_searching_by_invalid_pesel(self, client):
        response = client.get("/api/personal_accounts/00000000000")
        assert response.status_code == 404

    def test_update_account(self, client):
        data = {"first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901"}
        client.post("/api/personal_accounts", json=data)

        update_data = {"first_name": "Adam", "last_name": "Nowak"}
        response = client.patch("/api/personal_accounts/12345678901", json=update_data)
        assert response.status_code == 200

        get_response = client.get("/api/personal_accounts/12345678901")
        assert get_response.get_json()["first_name"] == "Adam"
        assert get_response.get_json()["last_name"] == "Nowak" 

    def test_delete_account(self, client):
        data = {"first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901"}
        client.post("/api/personal_accounts", json=data)

        response = client.delete("/api/personal_accounts/12345678901")
        assert response.status_code == 200
        assert len(account_registry.personal_accounts) == 0