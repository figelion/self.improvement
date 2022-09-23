import pytest


def test_deposition_made_for_account_adds_money_to_account() -> None:
    account = Account()
    amount = 500
    account.deposition(amount)

    assert account.balance == amount