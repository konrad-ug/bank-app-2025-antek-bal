from src.account import PersonalAccount, CompanyAccount

class TestPersonalAccount:
    def test_personal_account_creation_valid_pesel(self):
        # testing valid account
        account = PersonalAccount("John", "Doe", "06320302456")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "06320302456"
        
    def test_personal_account_creation_invalid_pesel_short(self):
        # testing account with invalid pesel (too short)
        account = PersonalAccount("Jane", "Smith", "4312")
        assert account.pesel == "invalid"

    def test_personal_account_creation_invalid_pesel_long(self):
        # testing account with invalid pesel (too long)
        account = PersonalAccount("Adam", "Wesley", "123234324112421")
        assert account.pesel == "invalid"

    def test_promo_code_valid(self):
        # testing valid promo code used by person born after 1960
        account = PersonalAccount("Jack", "Sparrow", "12345678912", "PROM_ABC")
        assert account.balance == 50
    
    def test_promo_code_invalid(self):
        # testing invalid promo code
        account = PersonalAccount("Mike", "Harris", "25521231323", "PROMOCODE")
        assert account.balance == 0
    
    def test_promo_code_invalid_sufix(self):
        # testing promo code invalid sufix
        account = PersonalAccount("Gregory", "Greg", "12345678912", "PROM_ABCD")
        assert account.balance == 0

    def test_promo_code_case_sensitive(self):
        # testing promo code in wrong case
        account = PersonalAccount("Spencer", "Pearl", "21234612291", "prom_ABC")
        assert account.balance == 0
    
    def test_promo_code_none(self):
        # testing account without promo code
        account = PersonalAccount("Jeffrey", "Dahmer", "13420234519")
        assert account.balance == 0
    
    def test_promo_code_valid_old(self):
        # testing valid promo code used by person born before 1960
        account = PersonalAccount("Sam", "Mean", "55032323234", "PROM_ABC")
        assert account.balance == 0
    
class TestCompanyAccount:
    def test_company_account_creation_valid_nip(self):
        # testing creating company account with valid nip
        account = CompanyAccount("Intel", "1234567891")
        assert account.company_name == "Intel"
        assert account.balance == 0
        assert account.nip == "1234567891"

    def test_company_account_creation_invalid_nip(self):
        # testing creating company account with invalid nip
        account = CompanyAccount("Microsoft", "124")
        assert account.nip == "invalid"

class TestTransfers:
    def test_transfer_valid(self):
        # testing valid outgoing transfer
        account1 = PersonalAccount("Julie", "Jensen", "93032323223", "PROM_ABC")
        account2 = PersonalAccount("Wilson", "Wood", "23114423950")

        account1.outgoing_transfer(account2, 35)

        assert account1.balance == 15
        assert account2.balance == 35
    
    def test_transfer_not_enough_money(self):
        # testing transfering more money than person obtain
        account1 = PersonalAccount("Julie", "Jensen", "93032323223", "PROM_ABC")
        account2 = PersonalAccount("Wilson", "Wood", "23114423950")

        account1.outgoing_transfer(account2, 100)

        assert account1.balance == 50
        assert account2.balance == 0

    def test_transfer_money_below_zero(self):
        # testing transfers with negative number of money
        account1 = PersonalAccount("Julie", "Jensen", "93032323223", "PROM_ABC")
        account2 = PersonalAccount("Wilson", "Wood", "23114423950")

        account1.outgoing_transfer(account2, -50)

        assert account1.balance == 50
        assert account2.balance == 0