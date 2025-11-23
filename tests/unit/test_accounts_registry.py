class TestAccountsRegistry:
    def test_add_personal_account(self, registry, personal_account_simple):
        assert personal_account_simple in registry.personal_accounts
        assert registry.quantity_personal_accounts() == 1

    def test_add_company_account(self, registry, company_account_first):
        assert company_account_first in registry.company_accounts
        assert registry.quantity_company_accounts() == 1

    def test_search_personal_account(self, registry, personal_account_simple):
        found = registry.search_personal_account("12345678901")
        assert found is personal_account_simple

        found_none = registry.search_personal_account("00000000000")
        assert found_none is None

    def test_search_company_account(self, registry, company_account_second):
        found = registry.search_company_account("Ryanair")
        assert found is company_account_second

        found_none = registry.search_company_account("Lufthansa")
        assert found_none is None

    def test_return_personal_accounts(self, registry, personal_account_simple, personal_account_valid):
        all_accounts = registry.return_personal_accounts()
        assert personal_account_simple in all_accounts and personal_account_valid in all_accounts
        assert len(all_accounts) == 2

    def test_return_company_accounts(self, registry, company_account_first, company_account_second):
        all_accounts = registry.return_company_accounts()
        assert company_account_first in all_accounts and company_account_second in all_accounts
        assert len(all_accounts) == 2

    def test_quantity_personal_and_company_accounts(self, registry, personal_account_simple, personal_account_valid, company_account_first):
        assert registry.quantity_personal_accounts() == 2
        assert registry.quantity_company_accounts() == 1
