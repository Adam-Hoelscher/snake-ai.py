class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        return Point(
            self.x - other.x,
            self.y - other.y
        )

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return (self.x, self.y) == (other.x, other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclid(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** .5

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))


Direction = [
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0)
]
# class Direction():
#     def __init__(self):
#         self.UP = Point(0, -1)
#         self.RIGHT = Point(1, 0)
#         self.DOWN = Point(0, 1)
#         self.LEFT = Point(-1, 0)
