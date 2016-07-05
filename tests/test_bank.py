import unittest
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

import bank

class TestBank(TestCase):
    def test_deposit(self):
        bank.balance = 0
        bank.deposit(100)

        self.assertEqual(bank.balance, 100)

    def test_withdraw(self):
        bank.balance = 100
        bank.withdraw(50)

        self.assertEqual(bank.balance, 50)