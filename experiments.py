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
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')



class Square():
    def square(self, x):
        return x*x

def hey():
    logger.debug('hello')



hey()
# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

a = 1348963479863478957324985734895739845
b = 1348963479863478957324985734895739845

print(str(id(a)) + '\n')
print(str(id(b)) + '\n')
