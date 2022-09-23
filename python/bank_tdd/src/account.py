from abc import ABC, abstractmethod


class BasicAccount(ABC):

    @abstractmethod
    def deposition(self, amount: int) -> None:
        raise NotImplemented


class Account(BasicAccount):

    def __init__(self):
        self._balance = 0

    @property
    def balance(self) -> int:
        return self._balance

    def deposition(self, amount: int) -> None:
        self._balance += amount
