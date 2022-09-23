import datetime
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.constance import ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE
from src.enums import Operation


@dataclass
class Statement:
    date: datetime.datetime
    amount: float
    operation: Operation
    balance: float


class BasicAccount(ABC):

    @abstractmethod
    def deposition(self, amount: int) -> None:
        raise NotImplemented

    @abstractmethod
    def withdraw(self, amount: int) -> int:
        raise NotImplemented


class OperationHistory():
    def __init__(self):
        self._history_of_operations: list[Statement] = []

        def _add_operation_to_history(self, function_name: str, amount: float) -> None:
            if function_name == "deposition":
                operation = Operation.DEPOSITION
            else:
                operation = Operation.WITHDRAWAL

            history_entry = Statement(date=datetime.datetime.now(), amount=amount, operation=operation)
            self._history_of_operations.append(history_entry)


class Account(BasicAccount):

    def __init__(self, operation_history_container: OperationHistory) -> None:
        self._balance = 0.
        self._history_of_operations: OperationHistory = operation_history_container

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def statement(self) -> list[Statement]:
        return self._history_of_operations

    def _add_operation_to_history(self, function_name: str, amount: float) -> None:
        if function_name == "deposition":
            operation = Operation.DEPOSITION
        else:
            operation = Operation.WITHDRAWAL

        history_entry = Statement(date=datetime.datetime.now(), amount=amount, operation=operation)
        self._history_of_operations.append(history_entry)

    @classmethod
    def save_operation(cls, function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            cls._add_operation_to_history(self=function.__parent__, function.__name__, *args, **kwargs)
            return result

        return wrapper()

    @save_operation(self)
    def deposition(self, amount: float) -> None:
        self._balance += amount

    @save_operation
    def withdraw(self, amount: float) -> float:
        if amount > self._balance:
            raise ValueError(ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE)
        self._balance -= amount
        return amount

