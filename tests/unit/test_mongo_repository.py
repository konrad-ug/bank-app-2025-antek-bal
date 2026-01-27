import unittest
from unittest.mock import MagicMock
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoRepository(unittest.TestCase):
    def test_save_all_clears_and_inserts(self):
        repo = MongoAccountsRepository()
        mock_collection = MagicMock()
        repo.collection = mock_collection

        account = PersonalAccount("Jan", "Kowalski", "12345678901")

        repo.save_all([account])

        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_many.assert_called()