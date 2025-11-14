class TestTransfers:
    def test_transfer_valid(self, personal_account_valid, personal_account_simple):
        # testing valid outgoing transfer
        personal_account_valid.outgoing_transfer(personal_account_simple, 35)

        assert personal_account_valid.balance == 15
        assert personal_account_simple.balance == 35

        assert personal_account_valid.history == [-35]
        assert personal_account_simple.history == [35]
    
    def test_transfer_not_enough_money(self, personal_account_valid, personal_account_simple):
        # testing transfering more money than person obtain
        personal_account_valid.outgoing_transfer(personal_account_simple, 100)

        assert personal_account_valid.balance == 50
        assert personal_account_simple.balance == 0

        assert personal_account_valid.history == []
        assert personal_account_simple.history == []

    def test_transfer_money_below_zero(self, personal_account_valid, personal_account_simple):
        # testing transfers with negative number of money
        personal_account_valid.outgoing_transfer(personal_account_simple, -50)

        assert personal_account_valid.balance == 50
        assert personal_account_simple.balance == 0

        assert personal_account_valid.history == []
        assert personal_account_simple.history == []

    def test_express_transfer_valid_personal(self, personal_account_valid, personal_account_simple):
        # testing valid express transfer for personal account

        personal_account_valid.express_transfer(personal_account_simple, 40)

        assert personal_account_valid.balance == 9
        assert personal_account_simple.balance == 40

        assert personal_account_valid.history == [-40, -1]
        assert personal_account_simple.history == [40]

    def test_express_transfer_valid_company(self, company_account_first, company_account_second):
        # testing valid express transfer for company account
        company_account_first.balance = 50

        company_account_first.express_transfer(company_account_second, 30)

        assert company_account_first.balance == 15
        assert company_account_second.balance == 30

        assert company_account_first.history == [-30, -5]
        assert company_account_second.history == [30]
    
    def test_express_transfer_not_enough_money_personal(self, personal_account_valid, personal_account_simple):
        # testing express transfer when trying to send more money than personal account has
        personal_account_valid.express_transfer(personal_account_simple, 1000)
        
        assert personal_account_valid.balance == 50
        assert personal_account_simple.balance == 0

        assert personal_account_valid.history == []
        assert personal_account_simple.history == []
    
    def test_express_transfer_money_below_zero_personal(self, personal_account_valid, personal_account_simple):
        # testing express transfer with negative number of money with personal account
        personal_account_valid.express_transfer(personal_account_simple, -50)

        assert personal_account_valid.balance == 50
        assert personal_account_simple.balance == 0

        assert personal_account_valid.history == []
        assert personal_account_simple.history == []
    
    def test_express_transfer_not_enough_money_company(self, company_account_first, company_account_second):
        # testing express transfer when trying to send more money than company account has

        company_account_first.express_transfer(company_account_second, 1000)

        assert company_account_first.balance == 0
        assert company_account_second.balance == 0

        assert company_account_first.history == []
        assert company_account_second.history == []
    
    def test_express_transfer_money_below_zero_company(self, company_account_first, company_account_second):
        # testing express transfer with negative number of money with company acocunt

        company_account_first.express_transfer(company_account_second, -50)

        assert company_account_first.balance == 0
        assert company_account_second.balance == 0

        assert company_account_first.history == []
        assert company_account_second.history == []