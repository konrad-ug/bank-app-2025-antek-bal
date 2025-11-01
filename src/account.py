class BaseAccount:
    def __init__(self):
        self.balance = 0

    def outgoing_transfer(self, receiver, amount):
        if amount > self.balance or amount <= 0:
            return False
        
        self.balance -= amount
        receiver.incoming_transfer(amount)
        
        return True

    def incoming_transfer(self, amount):
        self.balance += amount
        return True # pragma: no cover

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

    @staticmethod
    def is_born_after_60(pesel):
        if pesel == "invalid":
            return False
        
        year_prefix = int(pesel[0:2])
        month = int(pesel[2:4])
        full_year = (2000 if month > 20 else 1900) + year_prefix
        return full_year > 1960
    
    def express_transfer(self, receiver, amount):
        if amount > self.balance or amount <= 0:
            return False
        
        self.balance -= amount + 1
        receiver.incoming_transfer(amount)
        
        return True
        
class CompanyAccount(BaseAccount):
    def __init__(self, company_name, nip):
        super().__init__()

        self.company_name = company_name
        if len(nip) != 10:
            nip = "invalid"
        self.nip = nip
    
    def express_transfer(self, receiver, amount):
        if amount > self.balance or amount <= 0:
            return False
        
        self.balance -= amount + 5
        receiver.incoming_transfer(amount)
        
        return True