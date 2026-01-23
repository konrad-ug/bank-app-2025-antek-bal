import pytest

@pytest.fixture(autouse=True)
def mock_external_api_globally(mocker):
    mocker.patch("src.company_account.CompanyAccount.validate_nip", return_value=True)