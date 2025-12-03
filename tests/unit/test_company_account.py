import pytest
from src.company_account import CompanyAccount

@pytest.mark.parametrize(
    "company_name, nip, expected_nip",
    [
        ("Intel", "1234567891", "1234567891"),
        ("Microsoft", "124", "invalid"),
        ("AMD", "1234567899923492349", "invalid"),
        ("Nvidia", "one", "invalid")
    ]
)
def test_company_account_creation(company_name, nip, expected_nip):
    account = CompanyAccount(company_name, nip)
    assert account.company_name == company_name
    assert account.balance == 0
    assert account.nip == expected_nip
    assert account.history == []
