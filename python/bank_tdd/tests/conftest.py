import pytest

from src.account import Account, OperationHistory


@pytest.fixture(scope="function")
def basic_account() -> Account:
    return Account(history_container=OperationHistory())
