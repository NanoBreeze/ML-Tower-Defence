'''
import logging

def coolios():

    logger.info('hi')
    logger.debug('hey')


logger = logging.getLogger('testing file')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(module)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('new_log.log')
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

coolios()







'''

def hey():
    logger.debug('hello')

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

hey()
# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
