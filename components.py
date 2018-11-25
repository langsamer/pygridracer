from utils import Point


class CurrentPosition(Point):
    def __init__(self, x, y):
        super().__init__(x, y)


class NextPosition(Point):
    def __init__(self, x, y):
        super().__init__(x, y)


class Velocity:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy


