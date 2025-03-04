"""
bank_account.py - This module contains a class that represents a bank account.
The account supports deposit, withdraw, and get_balance operations.
Serialization and deserialization of the account is implemented using json.

Author: Autumn Peterson
Date: 24 Feb. 2025

*Disclaimer*
I used chatgpt.com to help me with what it means to and how to serialize and deserialize a
json file. This helped me write the to_json and from_json methods
I also used stackoverflow.com to help me implement the 'raise' statement when raising ValueErrors
I also used the Python Black linter to clean up my code.
"""

import json


class BankAccount:
    """A simple BankAccount class with methods to deposit, withdraw, and get_balance."""

    def __init__(self, account_number: int, balance: float = 0, owner: str = ""):
        """Initialize a BankAccount with an owner and an optional starting balance."""
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transaction_history = (
            []
        )  # store history of transactions in a list that can be added to to a dict

    def set_balance(self, initial_balance: int) -> None:
        """Sets bank account and ensures it cannot be negative"""
        if initial_balance < 0:
            raise ValueError("Invalid Balance: Bank Balance must be positive")
        self.balance = initial_balance

    def from_json(self) -> dict | None:
        """Deserialize a BankAccount object from a json file."""
        try:
            with open(f"bank_statement_{self.account_number}.json") as file:
                bank_dict = json.load(
                    file
                )  # use load to load from file (not loads because that loads from string)
                self.balance = bank_dict["balance"]
                self.transaction_history = bank_dict["transactions"]
                print(
                    f"Loaded account #{self.account_number} with balance: ${self.balance}"
                )
                return bank_dict

        except OSError as e:
            print(e)
            return None

    def to_json(self)->None:
        """Serialize a BankAccount object to a json file."""
        bank_json = dict(
            account_number=self.account_number,
            balance=self.balance,
            transactions=self.transaction_history,
        )

        try:
            with open(f"bank_statement_{self.account_number}.json", "w") as file:
                json.dump(bank_json, file, indent=4)

        except OSError as e:
            print(e)
            quit()

    def deposit(self, amount: float) -> None:
        """Deposit a positive amount to the account."""
        if amount <= 0:
            print("\nERROR: insufficient funds\n")
            raise ValueError("ERROR: insufficient funds")

        else:
            self.balance = self.balance + amount

            self.transaction_history.append(
                dict(transaction_type="Deposit", amount=amount)
            )  # save transaction to transaction_history list
            self.to_json()  # convert to json

    def withdraw(self, amount: float) -> None | ValueError:
        """Withdraw a positive amount if sufficient balance exists."""
        if self.balance - amount < 0 or amount <= 0:
            print("\nERROR: insufficient funds\n")
            raise ValueError("ERROR: insufficient funds")

        else:
            self.balance = self.balance - amount

            self.transaction_history.append(
                dict(transaction_type="Withdraw", amount=amount)
            )  # save transaction to transaction_history list
            self.to_json()  # convert to json

    def get_balance(self):
        """Return the current balance."""
        print(f"Current Balance: {self.balance}")
        return self.balance

    def show_transactions(self):
        """Prints all account transactions."""
        bank_json = self.from_json()
        print(f"========== Transaction History =============")
        for t in bank_json["transactions"]:
            print(t)
            print()
