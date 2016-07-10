import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')


class Path:
    """Represents the path a balloon will take"""

    def __init__(self):
        self.points = [(100, y) for y in range(30, 360)]

    def __len__(self):
        return len(self.points)

    def __getitem__(self, position):
        """
        :param position: int or slice (eg, 5:), used as the element inside the [ ] operators
        :return: self.points[position]
        """
        return self.points[position]
