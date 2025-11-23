class BaseAccount:
    def __init__(self):
        self.balance = 0
        self.history = []

    def outgoing_transfer(self, receiver, amount):
        if amount > self.balance or amount <= 0:
            return False
        
        self.balance -= amount
        self.add_to_history(-amount, "receiver", receiver)
        receiver.incoming_transfer(amount, self)
        
        return True

    def incoming_transfer(self, amount, sender):
        self.balance += amount
        self.add_to_history(amount, "sender", sender)
        
        return True # pragma: no cover

    def add_to_history(self, amount, unit_type, identity):
        self.history.append(
            {
                "id": len(self.history) + 1,
                "amount": amount,
                "type": unit_type,
                "identity": identity
            }
        )

class PersonalAccount(BaseAccount):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        if len(pesel) != 11:
            pesel = "invalid"
        self.pesel = pesel
        if promo_code:
            if promo_code.startswith("PROM_") and len(promo_code) == 8 and self.is_born_after_60(self.pesel):
                self.balance += 50
        accounts_registry.add_personal_account(self)
    
    def express_transfer(self, receiver, amount):
        if amount > self.balance or amount <= 0:
            return False
        
        self.balance -= amount + 1
        receiver.incoming_transfer(amount, self)

        self.add_to_history(-amount, "receiver", receiver)
        self.add_to_history(-1, "charge", "express transfer")

        
        return True
    
    def submit_for_loan(self, amount):
        last_three_incoming = len(self.history[-3:]) >= 3 and all(x["amount"] > 0 for x in self.history[-3:])
        last_five_sum = len(self.history) >= 5 and sum(x["amount"] for x in self.history[-5:]) > amount

        if last_three_incoming or last_five_sum:
            self.balance += amount
            self.add_to_history(amount, "sender", "official bank")
            return True
        
        return False
    
    @staticmethod
    def is_born_after_60(pesel):
        if pesel == "invalid":
            return False
        
        year_prefix = int(pesel[0:2])
        month = int(pesel[2:4])
        full_year = (2000 if month > 20 else 1900) + year_prefix
        return full_year > 1960
        
class CompanyAccount(BaseAccount):
    def __init__(self, company_name, nip):
        super().__init__()

        self.company_name = company_name
        if len(nip) != 10:
            nip = "invalid"
        self.nip = nip
        accounts_registry.add_company_account(self)
    
    def express_transfer(self, receiver, amount):
        if amount > self.balance or amount <= 0:
            return False
        
        self.balance -= amount + 5
        receiver.incoming_transfer(amount, self)
        
        self.add_to_history(-amount, "receiver", receiver)
        self.add_to_history(-5, "charge", "express transfer")
        
        return True
    
    def submit_for_loan(self, amount):
        filtered_history = [
            t for t in self.history
            if t["amount"] == -1775 
            and t["type"] == "receiver"
            and isinstance(t["identity"], CompanyAccount)
            and t["identity"].company_name == "ZUS"
        ]
                                       
        if len(filtered_history) > 0 and self.balance >= 2*amount:
            self.balance += amount
            self.add_to_history(amount, "sender", "official bank")
            return True
        return False
    
class AccountsRegistry:
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
    
    def search_company_account(self, name):
        return next((acc for acc in self.company_accounts if acc.company_name == name), None)
    
    def return_personal_accounts(self):
        return self.personal_accounts
    
    def return_company_accounts(self):
        return self.company_accounts
    
    def quantity_personal_accounts(self):
        return len(self.personal_accounts)
    
    def quantity_company_accounts(self):
        return len(self.company_accounts)
    
accounts_registry = AccountsRegistry()