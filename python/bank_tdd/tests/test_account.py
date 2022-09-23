import datetime

import pytest

from src.account import Account
from src.constance import ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE


def test_deposition_made_for_account_adds_money_to_account(basic_account) -> None:
    amount = 500
    basic_account.deposition(amount)

    assert basic_account.balance == amount


def test_withdraw_money_from_account_returns_money(basic_account) -> None:
    basic_account.deposition(100)
    withdraw_money = basic_account.withdraw(50)

    assert withdraw_money == 50


def test_withdraw_money_from_account_updates_state_of_account(basic_account) -> None:
    basic_account.deposition(100)
    basic_account.withdraw(50)

    assert basic_account.balance == 50


def test_withdraw_money_from_empty_account_raise_en_error(basic_account) -> None:
    with pytest.raises(ValueError, match=ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE):
        withdraw_money = basic_account.withdraw(50)


def test_account_provides_history_of_operations(basic_account) -> None:
    account = Account()
    account.deposition(500)
    account.withdraw(100)

    statement = account.statement

    assert statement[0].date == datetime.datetime.now()
    assert statement[0].amount == 500
    assert statement[0].operation == "DEPOSITION"
    assert statement[0].balance == 500

    assert statement[1].date == datetime.datetime.now()
    assert statement[1].amount == 100
    assert statement[1].operation == "WITHDRAWAL"
    assert statement[1].balance == 400

