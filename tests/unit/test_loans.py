class TestLoans:
    def test_loan_valid_last_three_transactions(self, personal_account_simple):
        # testing valid submittion for loan (3 last transactions are incoming)
        for _ in range(3):
            personal_account_simple.incoming_transfer(500)

        personal_account_simple.submit_for_loan(4000)

        assert personal_account_simple.balance == 5500
    
    def test_loan_valid_last_five_transactions(self, personal_account_simple, other_personal_account_simple):
        # testing valid submittion for loan (sum of last 5 transactions is higher than loan)
        for _ in range(2):
            personal_account_simple.incoming_transfer(2000)

        for _ in range(3):
            personal_account_simple.outgoing_transfer(other_personal_account_simple, 300)
        
        personal_account_simple.submit_for_loan(3000)

        assert personal_account_simple.balance == 6100
        assert personal_account_simple.history == [2000, 2000, -300, -300, -300, 3000]
    
    def test_loan_valid_last_five_transactions_with_express_transfer(self, personal_account_simple, other_personal_account_simple):
        # testing valid submittion for loan (sum of last 5 transactions is higher than loan)
        personal_account_simple.incoming_transfer(20000)

        for _ in range(2):
            personal_account_simple.express_transfer(other_personal_account_simple, 300)
        
        personal_account_simple.submit_for_loan(19000)

        assert personal_account_simple.balance == 38398
        assert personal_account_simple.history == [20000, -300, -1, -300, -1, 19000]
    
    def test_loan_invalid_less_than_five_transactions(self, personal_account_simple):
        # testing invalid submittion for loan (less than 5 transactions in history)
        personal_account_simple.incoming_transfer(50000)

        personal_account_simple.submit_for_loan(10000)

        assert personal_account_simple.balance == 50000
        assert personal_account_simple.history == [50000]
    
    def test_loan_invalid_loan_higher_than_transactions(self, personal_account_simple, other_personal_account_simple):
        # testing invalid submittion for loan (sum of last transactions is less than loan)
        for _ in range(2):
            personal_account_simple.incoming_transfer(2000)

        for _ in range(3):
            personal_account_simple.outgoing_transfer(other_personal_account_simple, 300)
        
        personal_account_simple.submit_for_loan(100000)

        assert personal_account_simple.balance == 3100
        assert personal_account_simple.history == [2000, 2000, -300, -300, -300]