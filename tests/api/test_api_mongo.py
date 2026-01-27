import unittest
from unittest.mock import patch, MagicMock
from src.personal_account import PersonalAccount


class TestApiPersistence(unittest.TestCase):
    def setUp(self):
        from app.api import app
        self.app = app
        self.client = self.app.test_client()

    @patch('app.api.account_repository')
    @patch('app.api.account_registry')
    def test_save_accounts_calls_repo_save(self, mock_registry, mock_repository):
        mock_accounts = [
            PersonalAccount("Jan", "Kowalski", "12345678901"),
            PersonalAccount("Anna", "Nowak", "12345678902")
        ]
        mock_registry.return_personal_accounts.return_value = mock_accounts

        response = self.client.post('/api/accounts/save')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Accounts saved successfully"})

        mock_repository.save_all.assert_called_once_with(mock_accounts)

    @patch('app.api.account_repository')
    @patch('app.api.account_registry')
    def test_load_accounts_clears_registry_and_loads_from_repo(self, mock_registry, mock_repository):
        loaded_account = PersonalAccount("Anna", "Nowak", "99999999999")
        mock_repository.load_all.return_value = [loaded_account]

        response = self.client.post('/api/accounts/load')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["count"], 1)

        mock_registry.clear.assert_called_once()

        mock_repository.load_all.assert_called_once()

        mock_registry.add_personal_account.assert_called_with(loaded_account)