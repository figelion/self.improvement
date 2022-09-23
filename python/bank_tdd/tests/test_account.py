import pytest

from src.account import Account


def test_deposition_made_for_account_adds_money_to_account() -> None:
    account = Account()
    amount = 500
    account.deposition(amount)

    assert account.balance == amount


def test_withdraw_money_from_account_returns_money() -> None:
    account = Account()
    account.deposition(100)
    withdraw_money = account.withdraw(50)

    assert withdraw_money == 50


def test_withdraw_money_from_account_updates_state_of_account() -> None:
    account = Account()
    account.deposition(100)
    account.withdraw(50)

    assert account.balance == 50

def test_withdraw_money_from_empty_account_raise_en_error() -> None:
    account = Account()
    with pytest.raises(Exception):
        withdraw_money = account.withdraw(50)
