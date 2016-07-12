import message_buffer
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

    # if client & server, they will use this value balance from message_buffer. If solo, adding this to message_buffer doesn't affect game play
    # thus, add new balance to message_buffer
    message_buffer.push_lifepoint_message(life_balance)


def decrease(amount=1):
    """
    :param amount: int, decreases the specified amount of money to the balance
    """

    assert isinstance(amount, int), 'amount must be an integer'

    global life_balance
    life_balance -= amount

    # if client & server, they will use this value balance from message_buffer. If solo, adding this to message_buffer doesn't affect game play
    # thus, add new balance to message_buffer
    message_buffer.push_lifepoint_message(life_balance)
