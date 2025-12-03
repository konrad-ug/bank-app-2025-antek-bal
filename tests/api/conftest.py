import pytest
from app.api import app, account_registry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_registry():
    account_registry.personal_accounts = []
    account_registry.company_accounts = []