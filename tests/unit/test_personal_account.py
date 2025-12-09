import pytest
from src.personal_account import PersonalAccount

@pytest.mark.parametrize(
    "first_name, last_name, pesel, promo_code, expected_balance",
    [
        ("John", "Doe", "06320302456", None, 0),
        ("Jack", "Sparrow", "12345678912", "PROM_ABC", 50),
        ("Sam", "Mean", "55032323234", "PROM_ABC", 0)
    ]
)
def test_personal_account_creation(first_name, last_name, pesel, promo_code, expected_balance):
    account = PersonalAccount(first_name, last_name, pesel, promo_code)
    assert account.first_name == first_name
    assert account.last_name == last_name
    assert account.pesel == pesel
    assert account.balance == expected_balance

def test_personal_account_invalid_pesel(invalid_pesel):
    account = PersonalAccount("Jane", "Smith", invalid_pesel)
    assert account.pesel == "invalid"

def test_personal_account_invalid_promo(invalid_promo_code):
    account = PersonalAccount("Mike", "Harris", "25521231323", invalid_promo_code)
    assert account.balance == 0