import datetime
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.constance import ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE
from src.enums import Operation


@dataclass
class Statement:
    date: datetime.date
    amount: float
    operation: Operation


class AccountInterface(ABC):

    @abstractmethod
    def deposition(self, amount: int) -> None:
        raise NotImplemented

    @abstractmethod
    def withdraw(self, amount: int) -> int:
        raise NotImplemented


class OperationHistory:
    def __init__(self):
        self._history_of_operations: list[Statement] = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _add_operation_to_history(self, function_name: str, amount: float) -> None:
        if function_name == "_deposition":
            operation = Operation.DEPOSITION
        else:
            operation = Operation.WITHDRAWAL

        history_entry = Statement(date=datetime.datetime.now().date(), amount=amount, operation=operation)
        self._history_of_operations.append(history_entry)

    def save_account_operation(self, function, *args, **kwargs):
        result = function(*args, **kwargs)
        self._add_operation_to_history(function.__name__, *args, **kwargs)
        return result

    @property
    def history(self):
        return self._history_of_operations


class Account(AccountInterface):

    def __init__(self, history_container: OperationHistory) -> None:
        self._balance = 0.
        self.history_container = history_container

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def statement(self) -> list[Statement]:
        return self.history_container.history

    def deposition(self, amount: float) -> None:
        def _deposition(amount):
            self._balance += amount

        with self.history_container as operation_register:
            operation_register.save_account_operation(_deposition, amount)

    def withdraw(self, amount: float) -> float:
        def _withdraw(amount: int):
            if amount > self._balance:
                raise ValueError(ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE)
            self._balance -= amount
            return amount

        with self.history_container as operation_register:
            withdraw_money = operation_register.save_account_operation(_withdraw, amount)

        return withdraw_money
