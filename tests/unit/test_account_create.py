from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", 0, '05291201356', 'XYZ')
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert len(account.pesel) == 11
        if (account.promo_code == 'XYZ'):
            assert account.balance == 50
        else:
            assert account.balance == 0


