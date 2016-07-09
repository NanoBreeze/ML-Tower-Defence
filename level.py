import logging
import logging.config
import path
import balloon

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')


class Level:
    """Base class for all levels. A level represents the ballons to display and on which path they go on"""

    def __init__(self, numbers_representing_balloons, balloon_path):
        """stores the numbers_representing_balloons and the path they are all on"""
        self.numbers_representing_balloons = numbers_representing_balloons
        self.balloon_path = balloon_path

    def map_number_to_balloon(self, number, balloon_path):
        """
        :param number: int, represents the number of layers the balloon is to have
        :param balloon_path: the path the balloon is to be on
        Returns the balloon corresponding to the specified number
        :return:
        """

        assert isinstance(number, int) and 1 <= number <= 5, 'number must be an integer from 1 to 5'

        if number == 1:
            return balloon.create_balloon_context(balloon.BALLOON_L1, balloon_path)
        elif number == 2:
            return balloon.create_balloon_context(balloon.BALLOON_L2, balloon_path)
        elif number == 3:
            return balloon.create_balloon_context(balloon.BALLOON_L3, balloon_path)
        elif number == 4:
            return balloon.create_balloon_context(balloon.BALLOON_L4, balloon_path)
        elif number == 5:
            return balloon.create_balloon_context(balloon.BALLOON_L5, balloon_path)

        raise NotImplementedError('the specified number mapping to balloon doesnt exist. How did it pass the assertion?')

    def get_next_balloon_context(self):
        """
        :return: balloon_context or None.
         Returns the next balloon to display on to the path on the game. The balloon list uses numbers so we convert it to a balloon context
        """
        if self.numbers_representing_balloons:
            current_number_representing_balloon = self.numbers_representing_balloons.pop(0)
            return self.map_number_to_balloon(current_number_representing_balloon, self.balloon_path)
        return None

    def there_are_more_balloons_to_display(self):
        """Determines if all the balloons on this level have been displayed on screen"""
        if self.numbers_representing_balloons:
            return True
        return False



class Level1(Level):
    def __init__(self):
        logger.debug('Level1 started')
        balloon_path = path.Path()
        # the balloons to output on this level
        numbers_representing_balloons = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        super().__init__(numbers_representing_balloons, balloon_path)

class Level2(Level):
    def __init__(self):
        balloon_path = path.Path()
        # the balloons to output on this level
        numbers_representing_balloons = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        super().__init__(numbers_representing_balloons, balloon_path)

class Level3(Level):
    def __init__(self):
        logger.debug('Level3 started')
        balloon_path = path.Path()
        # the balloons to output on this level
        numbers_representing_balloons = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        super().__init__(numbers_representing_balloons, balloon_path)

