class TestBaseAccount:
    def test_base_account_creation(self, base_account):
        assert base_account.balance == 0
        assert base_account.history == []
