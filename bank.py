import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')


balance = 0 #amount of money user currently has

def deposit(amount):
    """
    :param amount: int, adds the specified amount of money to the balance
    """

    assert isinstance(amount, int), 'amount must be an integer'

    global balance
    balance += amount


def withdraw(amount):
    """
    :param amount: int, decreases the specified amount of money to the balance
    """

    assert isinstance(amount, int), 'amount must be an integer'

    global balance
    balance -= amount


def report_financial():
    """
    logs the balance
    """
    global balance
    logger.info('Balance: {0} \n'
          .format(balance))



