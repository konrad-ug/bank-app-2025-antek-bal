import pytest
from src.company_account import CompanyAccount
from datetime import datetime


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

    def test_send_history_via_email_success(self, mocker):
        mocker.patch("src.company_account.CompanyAccount.validate_nip", return_value=True)
        mock_smtp = mocker.patch("src.company_account.SMTPClient")
        mock_smtp.send.return_value = True

        account = CompanyAccount("Company", "1234567890")
        account.add_to_history(5000, "sender", "Client Invoice")

        email = "ceo@company.com"
        result = account.send_history_via_email(email)

        assert result is True

        expected_date = datetime.now().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {expected_date}"
        expected_text = "Company account history: [5000]"

        mock_smtp.send.assert_called_once_with(expected_subject, expected_text, email)

    def test_send_history_via_email_failure(self, mocker):
        mocker.patch("src.company_account.CompanyAccount.validate_nip", return_value=True)
        mock_smtp = mocker.patch("src.company_account.SMTPClient")
        mock_smtp.send.return_value = False

        account = CompanyAccount("Company", "1234567890")

        assert account.send_history_via_email("ceo@company.com") is False
