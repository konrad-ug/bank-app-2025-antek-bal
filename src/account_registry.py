from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class AccountRegistry:
    def __init__(self):
        self.personal_accounts = []
        self.company_accounts = []
    
    def add_personal_account(self, account: PersonalAccount):
        self.personal_accounts.append(account)
        return True

    def add_company_account(self, account: CompanyAccount):
        self.company_accounts.append(account)
        return True
    
    def search_personal_account(self, pesel):
        return next((acc for acc in self.personal_accounts if acc.pesel == pesel), None)
    
    def search_company_account(self, nip):
        return next((acc for acc in self.company_accounts if acc.nip == nip), None)
    
    def return_personal_accounts(self):
        return self.personal_accounts
    
    def return_company_accounts(self):
        return self.company_accounts
    
    def quantity_personal_accounts(self):
        return len(self.personal_accounts)
    
    def quantity_company_accounts(self):
        return len(self.company_accounts)