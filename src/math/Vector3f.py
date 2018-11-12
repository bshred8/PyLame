class Vector4f:

    x:float = None
    y:float = None
    z:float = None

    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def triangleArea(self, b, c):
        x1:float = b.x - self.x
        y1:float = b.y - self.y
        x2:float = c.x - self.x
        y2:float = c.y - self.y

        return (x1 * y2 - x2 * y1)
