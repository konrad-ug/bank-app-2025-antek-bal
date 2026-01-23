import pytest
from src.company_account import CompanyAccount


class TestCompanyAccount:
    def test_create_account_valid_nip(self, mocker):
        mocker.patch("src.company_account.CompanyAccount.validate_nip", return_value=True)

        account = CompanyAccount("Valid Company", "1234567890")

        assert account.nip == "1234567890"
        assert account.company_name == "Valid Company"

    def test_create_account_invalid_nip_raises_error(self, mocker):
        mocker.patch("src.company_account.CompanyAccount.validate_nip", return_value=False)

        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Fake Company", "1234567890")

    def test_create_account_api_error(self, mocker):
        mocker.patch("src.company_account.CompanyAccount.validate_nip", return_value=False)

        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Error Company", "1234567890")

    @pytest.mark.parametrize("nip", ["123", "12345678901", "invalid"])
    def test_create_account_wrong_length_does_not_call_api(self, mocker, nip):
        mock_validate = mocker.patch("src.company_account.CompanyAccount.validate_nip")

        account = CompanyAccount("Bad Len Corp", nip)

        assert account.nip == "invalid"
        mock_validate.assert_not_called()