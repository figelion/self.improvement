from abc import ABC, abstractmethod

from src.constance import ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE


class BasicAccount(ABC):

    @abstractmethod
    def deposition(self, amount: int) -> None:
        raise NotImplemented

    @abstractmethod
    def withdraw(self, amount: int) -> int:
        raise NotImplemented


class Account(BasicAccount):

    def __init__(self):
        self._balance = 0.

    @property
    def balance(self) -> int:
        return self._balance

    def deposition(self, amount: int) -> None:
        self._balance += amount

    def withdraw(self, amount: int) -> int:
        if amount > self._balance:
            raise ValueError(ERROR_MESSAGE_WITHDRAW_EXCEEDS_BALANCE)
        self._balance -= amount
        return amount
