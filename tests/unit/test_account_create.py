from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", 0, '05291201356')
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert len(account.pesel) == 11

