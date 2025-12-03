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