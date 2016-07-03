import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')


balance = 0

def deposit(amount):
    global balance
    balance += amount
    print('Deposited {0}. Current balance is {1}'.format(amount, balance))


def withdraw(amount):
    """Decrease balance"""
    global balance
    balance -= amount


def report_financial(self):
    """Prints the financial statement for the bank"""
    global balance
    logger.info('Balance: {0} \n'
          .format(balance))



