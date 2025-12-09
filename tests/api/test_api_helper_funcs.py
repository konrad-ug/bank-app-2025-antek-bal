import pytest
from app.api import find_receiver, account_registry
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestFindReceiver:
    @pytest.fixture(autouse=True)
    def clean_registry(self):
        account_registry.personal_accounts = []
        account_registry.company_accounts = []
        yield
        account_registry.personal_accounts = []
        account_registry.company_accounts = []

    def test_find_receiver_pesel(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account_registry.add_personal_account(account)

        data = {"receiver_pesel": "12345678901"}
        result = find_receiver(data)

        assert result == account

    def test_find_receiver_nip(self):
        account = CompanyAccount("Firma", "1234567890")
        account_registry.add_company_account(account)

        data = {"receiver_nip": "1234567890"}
        result = find_receiver(data)

        assert result == account

    def test_find_receiver_none_keys(self):
        data = {"other_key": "value"}
        result = find_receiver(data)

        assert result is None

    def test_find_receiver_not_found(self):
        data = {"receiver_pesel": "00000000000"}
        result = find_receiver(data)

        assert result is None