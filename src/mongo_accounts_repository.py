from pymongo import MongoClient
from src.personal_account import PersonalAccount

class MongoAccountsRepository:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['bank_db']
        self.collection = self.db['accounts']

    def save_all(self, accounts):
        self.collection.delete_many({})

        documents = [account.to_dict() for account in accounts]
        if documents:
            self.collection.insert_many(documents)

    def load_all(self):
        documents = self.collection.find()
        accounts = []

        for d in documents:
            acc = PersonalAccount(d['first_name'], d['last_name'], d['pesel'])
            acc.balance = d['balance']
            acc.history = d['history']
            accounts.append(acc)

        return accounts