class Account:
    def __init__(self, first_name, last_name, balance, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        if (promo_code == 'XYZ'):
            self.balance = balance + 50
        else:
            self.balance = balance
        self.pesel = pesel
        self.promo_code = promo_code