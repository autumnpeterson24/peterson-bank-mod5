"""
test_bank_account.py - testing script that uses pytest in order to test the BankAccount class from bank_account.py
Author: Autumn Peterson
Date: 24 Feb. 2025

* Disclaimer *
I used geeksforgeeks.com to help me learn how to use the @pytest.fixture from pytest
as well as how to properly run the tests. I also used stackoverflow.com to help me
use the pytest.raises() method to check my raised ValueErrors
I also used the Python Black Linter to clean up my code

"""

import pytest
import json
from bank_account import BankAccount


@pytest.fixture
def bank_account() -> BankAccount:
    """Creating BankAccount to test class methods"""
    b = BankAccount(1111, 0)  # uses default amount of 0
    return b


def test_deposit_positive(bank_account):
    """Testing a normal deposit (positive test)"""
    bank_account.deposit(50)  # balance starts at zero and increases to 50 after deposit
    assert bank_account.balance == 50


def test_deposit_negative(bank_account):
    """Test a negative deposit which should raise a ValueError (negative test)"""
    with pytest.raises(ValueError):
        bank_account.deposit(-10)


def test_deposit_zero(bank_account):
    """Test a deposit of 0 with raises a ValueError"""
    with pytest.raises(ValueError):
        bank_account.deposit(0)


def test_withdraw_positive(bank_account):
    """Test a normal withdrawal from the account (positive test)"""
    bank_account.balance = 100  # set balance to 100 to test withdrawal function
    bank_account.withdraw(10)  # withdraw 10 to have balance of 90
    assert bank_account.balance == 90


def test_withdraw_negative(bank_account):
    """Test withdrawing a negative amount which should return a ValueError"""
    bank_account.balance = 100  # set balance to 100
    with pytest.raises(ValueError):
        bank_account.withdraw(-10)


def test_withdraw_zero(bank_account):
    """Test withdrawing a 0 amount which raises a ValueError"""
    with pytest.raises(ValueError):
        bank_account.withdraw(0)


def test_withdraw_over_balance(bank_account):
    """Test withdrawing an insufficient amount from the balance"""
    with pytest.raises(ValueError):
        bank_account.withdraw(100)


def test_get_balance(bank_account):
    """Test getting the balance from the bank account (default is zero)"""
    assert bank_account.get_balance() == 0


def test_negative_balance(bank_account):
    """Test trying to set a Bank Account with a negative value which raises a ValueError"""
    with pytest.raises(ValueError):
        bank_account.set_balance(-100)


def test_withdrawing_balance_to_zero(bank_account):
    """Testing withdrawing bank account to a balance of 0"""
    bank_account.set_balance(100)  # setting bank account to 100
    bank_account.withdraw(100)  # withdrawing 100 to get balance of 0
    assert bank_account.balance == 0


def test_to_json(bank_account):
    """Testing the to_json() function"""
    expected_json = {"account_number": 1111, "balance": 0, "transactions": []}

    bank_account.to_json()  # create a default json bank account file

    try:
        with open(f"bank_statement_{bank_account.account_number}.json") as file:
            assert (
                json.load(file) == expected_json
            )  # check the created json is equal to the expected json

    except IOError as e:
        print(e)


def test_from_json(bank_account):
    """Testing the from_json() function"""
    expected_json = {"account_number": 1111, "balance": 0, "transactions": []}

    bank_dict = bank_account.from_json()
    assert (
        expected_json == bank_dict
    )  # check that expected json is the same as json loaded using from_json()
