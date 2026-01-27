from src.base_account import BaseAccount
from src.smtp.smtp import SMTPClient
from datetime import datetime


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

    def send_history_via_email(self, email):
        date = datetime.now().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {date}"
        text = f"Personal account history: {[item['amount'] for item in self.history]}"

        return SMTPClient.send(subject, text, email)

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def is_born_after_60(pesel):
        if pesel == "invalid":
            return False

        year_prefix = int(pesel[0:2])
        month = int(pesel[2:4])
        full_year = (2000 if month > 20 else 1900) + year_prefix
        return full_year > 1960
