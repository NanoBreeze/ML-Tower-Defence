
class Path:
    """Represents the path a ballon will take"""
    def __init__(self):
        self.points = [(100, y) for y in range(50, 360)]

    def __len__(self):
        return len(self.points)

    def __getitem__(self, position):
        return self.points[position]