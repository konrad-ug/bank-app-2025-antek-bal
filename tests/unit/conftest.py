import pytest
from src.base_account import BaseAccount
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account_registry import AccountRegistry
from app.api import account_registry


@pytest.fixture
def base_account():
    return BaseAccount()

@pytest.fixture(params=["4312", "123234324112421"])
def invalid_pesel(request):
    return request.param

@pytest.fixture(params=["PROMOCODE", "PROM_ABCD", "prom_ABC", None])
def invalid_promo_code(request):
    return request.param

@pytest.fixture
def personal_account_valid():
    return PersonalAccount("John", "Doe", "06320302456", "PROM_ABC")

@pytest.fixture
def personal_account_simple():
    return PersonalAccount("Jack", "Sparrow", "12345678901")

@pytest.fixture
def other_personal_account_simple():
    return PersonalAccount("John", "Wilson", "12345678910")

@pytest.fixture
def company_account_first():
    return CompanyAccount("Wizzair", "1232567891")

@pytest.fixture
def company_account_second():
    return CompanyAccount("Ryanair", "9876543211")

@pytest.fixture
def zus_account():
    return CompanyAccount("ZUS", "1293922354")

@pytest.fixture
def registry():
    account_registry.personal_accounts = []
    account_registry.company_accounts = []
    return account_registry