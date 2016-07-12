import message_buffer

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

balance = 100  # amount of money user currently has


def deposit(amount):
    """
    :param amount: int, adds the specified amount of money to the balance
    """
    assert isinstance(amount, int), 'amount must be an integer'

    global balance
    balance += amount
    
    #if client & server, they will use this value balance from message_buffer. If solo, adding this to message_buffer doesn't affect game play
    #thus, add new balance to message_buffer
    message_buffer.push_bank_balance_message(balance)


def withdraw(amount):
    """
    :param amount: int, decreases the specified amount of money to the balance
    """
    assert isinstance(amount, int), 'amount must be an integer'

    global balance
    balance -= amount

    #if client & server, they will use this value balance from message_buffer. If solo, adding this to message_buffer doesn't affect game play
    #thus, add new balance to message_buffer
    message_buffer.push_bank_balance_message(balance)
