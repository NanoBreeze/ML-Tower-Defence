import logging

logging.basicConfig(level=logging.DEBUG)


class Singleton(type):
    """Metaclass for making a Singleton Bank object"""
    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)

        logging.debug('User attempted to instantiate a second Bank object. \
                      The Bank object is a Singleton and only the first Bank is created')
        return cls.instance


class Bank(metaclass=Singleton):
    """Represents the amount of money user has"""
    def __init__(self, initial_balance=0, interest=0):
        self.balance = initial_balance
        self.interest = interest

    def deposit(self, accounts_receivable):
        """Increase balance"""
        self.balance += accounts_receivable

    def withdraw(self, accounts_payable):
        """Decrease balance"""
        self.balance -= accounts_payable

    def report_financial(self):
        """Prints the financial statement for the bank"""
        print('Balance: {0} \n'
              'Interest: {1}'
              .format(self.balance, self.interest))




