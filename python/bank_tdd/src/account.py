from abc import ABC, abstractmethod


class BasicAccount(ABC):

    @abstractmethod
    def deposition(self, amount: int) -> None:
        raise NotImplemented

    @abstractmethod
    def withdraw(self, amount: int) -> int:
        raise NotImplemented


class Account(BasicAccount):

    def __init__(self):
        self._balance = 0

    @property
    def balance(self) -> int:
        return self._balance

    def deposition(self, amount: int) -> None:
        self._balance += amount

    def withdraw(self, amount: int) -> int:
        if amount > self._balance:
            raise ValueError("Cannot withdraw money: request amount is bigger then balance of the account")
        self._balance -= amount
        return amount
