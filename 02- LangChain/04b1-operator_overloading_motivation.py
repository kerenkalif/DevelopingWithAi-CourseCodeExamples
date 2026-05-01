class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def add(self, other):
        print(f"DEBUG: adding {self} with {other}")
        return Point(self.x + other.x, self.y + other.y)

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = Point(1, 1)

result = p1.add(p2).add(p3)
print(result)  # 5, 7
