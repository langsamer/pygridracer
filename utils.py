class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Point has only two members")


class Rectangle:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = min(x0, x1)
        self.y0 = min(y0, y1)
        self.x1 = max(x0, x1)
        self.y1 = max(y0, y1)

    def _contains(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def __contains__(self, item):
        x, y = item[0], item[1]
        return self._contains(x, y)
