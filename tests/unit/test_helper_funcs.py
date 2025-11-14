import pytest
from src.account import PersonalAccount

@pytest.mark.parametrize(
    "pesel, expected_return",
    [
        ("12325678901", True),
        ("59125678901", False),
        ("invalid", False)
    ]
)
def test_age_verification(pesel, expected_return):
    assert PersonalAccount.is_born_after_60(pesel) == expected_return