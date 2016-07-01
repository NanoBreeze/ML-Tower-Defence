
class Path:
    """Represents the path a ballon will take"""
    def __init__(self):
        self.points = [(100, y) for y in range(0, 360)]