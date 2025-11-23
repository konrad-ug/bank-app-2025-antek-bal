class TestLoans:
    def test_loan_valid_last_three_transactions_personal_account(self, personal_account_simple, other_personal_account_simple):
        # testing valid submittion for loan (3 last transactions are incoming)
        other_personal_account_simple.balance = 1500
        for _ in range(3):
            other_personal_account_simple.outgoing_transfer(personal_account_simple, 500)

        personal_account_simple.submit_for_loan(4000)

        assert personal_account_simple.balance == 5500
    
    def test_loan_valid_last_five_transactions_personal_account(self, personal_account_simple, other_personal_account_simple):
        # testing valid submittion for loan (sum of last 5 transactions is higher than loan)
        other_personal_account_simple.balance = 4000
        for _ in range(2):
            other_personal_account_simple.outgoing_transfer(personal_account_simple, 2000)

        for _ in range(3):
            personal_account_simple.outgoing_transfer(other_personal_account_simple, 300)
        
        personal_account_simple.submit_for_loan(3000)

        assert personal_account_simple.balance == 6100
    
    def test_loan_valid_last_five_transactions_with_express_transfer_personal_account(self, personal_account_simple, other_personal_account_simple):
        # testing valid submittion for loan (sum of last 5 transactions is higher than loan)
        other_personal_account_simple.balance = 20000
        other_personal_account_simple.outgoing_transfer(personal_account_simple, 20000)

        for _ in range(2):
            personal_account_simple.express_transfer(other_personal_account_simple, 300)
        
        personal_account_simple.submit_for_loan(19000)

        assert personal_account_simple.balance == 38398
    
    def test_loan_invalid_less_than_five_transactions_personal_account(self, personal_account_simple, other_personal_account_simple):
        # testing invalid submittion for loan (less than 5 transactions in history)
        other_personal_account_simple.balance = 50000
        other_personal_account_simple.outgoing_transfer(personal_account_simple, 50000)

        personal_account_simple.submit_for_loan(10000)

        assert personal_account_simple.balance == 50000
    
    def test_loan_invalid_loan_higher_than_transactions_personal_account(self, personal_account_simple, other_personal_account_simple):
        # testing invalid submittion for loan (sum of last transactions is less than loan)
        other_personal_account_simple.balance = 4000
        for _ in range(2):
            other_personal_account_simple.outgoing_transfer(personal_account_simple, 2000)

        for _ in range(3):
            personal_account_simple.outgoing_transfer(other_personal_account_simple, 300)
        
        personal_account_simple.submit_for_loan(100000)

        assert personal_account_simple.balance == 3100

    # ============================================================================================================================================

    def test_loan_valid_company_account(self, company_account_first, zus_account):
        # testing valid submittion for loan (both conditions are valid)
        company_account_first.balance = 51775
        company_account_first.outgoing_transfer(zus_account, 1775)

        company_account_first.submit_for_loan(25000)

        assert company_account_first.balance == 75000

    def test_loan_invalid_not_enough_money_company_account(self, company_account_first, zus_account):
        # testing invalid submittion for loan (only second condition is valid)
        company_account_first.balance = 51775
        company_account_first.outgoing_transfer(zus_account, 1775)

        company_account_first.submit_for_loan(30000)

        assert company_account_first.balance == 50000

    def test_loan_invalid_no_transfer_to_zus_company_account(self, company_account_first, company_account_second):
        # testing invalid submittion for loan (only first condition is valid)
        company_account_first.balance = 51775
        company_account_first.outgoing_transfer(company_account_second, 1775)

        company_account_second.submit_for_loan(25000)

        assert company_account_first.balance == 50000
    
    def test_loan_invalid_no_1775_transfer_to_zus(self, company_account_first, zus_account):
        # testing invalid submittion for loan (only first condition is valid)
        company_account_first.balance = 51774
        company_account_first.outgoing_transfer(zus_account, 1774)

        company_account_first.submit_for_loan(25000)

        assert company_account_first.balance == 50000
    
    def test_loan_invalid_both_conditions_wrong(self, company_account_first, company_account_second):
        # testing invalid submittion for loan (both conditions are wrong)
        company_account_first.balance = 51000
        company_account_first.outgoing_transfer(company_account_second, 1000)

        company_account_first.submit_for_loan(50000)

        assert company_account_first.balance == 50000

