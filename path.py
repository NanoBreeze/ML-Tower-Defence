import logging

logging.basicConfig(level=logging.DEBUG)

class Path:
    """Represents the path a ballon will take"""
    def __init__(self):
        self.points = [(100, y) for y in range(30, 360)]

    def __len__(self):
        return len(self.points)

    def __getitem__(self, position):
        """Used for slicing (tuple) as well as single index (integer)"""
        logging.debug('inside Path __getitem__. The position is: ' + str(position))
        return self.points[position]
