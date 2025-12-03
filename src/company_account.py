from src.base_account import BaseAccount

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