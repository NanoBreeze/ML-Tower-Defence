import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')


life_balance = 20 #amount of money user currently has

def increase(amount=1):
    """
    :param amount: int, adds the specified amount of money to the balance
    """

    assert isinstance(amount, int), 'amount must be an integer'

    global life_balance
    life_balance += amount


def decrease(amount=1):
    """
    :param amount: int, decreases the specified amount of money to the balance
    """

    assert isinstance(amount, int), 'amount must be an integer'

    global life_balance
    life_balance -= amount
