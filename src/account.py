class Account:
    def __init__(self, first_name, last_name, balance, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        if (promo_code == 'XYZ' and born_after_60(pesel)):
            self.balance = balance + 50
        else:
            self.balance = balance
        self.pesel = pesel
        self.promo_code = promo_code

def born_after_60(pesel):
    yy = int(pesel[0:2])
    if yy <= 25:
        year = 2000 + yy
    year = 1900 + yy
    
    return year > 1960