import pytest

from src.account import Account


@pytest.fixture(scope="module")
def basic_account() -> Account:
    return Account()
