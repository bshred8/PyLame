from math import *

class Vector4f:

    x:float = None
    y:float = None
    z:float = None
    w:float = None

    def __init__(self, x:float, y:float, z:float, w:float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def triangleArea(self, b, c):
        x1:float = b.x - self.x
        y1:float = b.y - self.y
        x2:float = c.x - self.x
        y2:float = c.y - self.y

        return (x1 * y2 - x2 * y1)

    def perspectiveDivide(self):
        return Vector4f(self.x / self.w, self.y / self.w, self.z / self.w, self.w)

    @classmethod
    def normalize(vecRight):
        length:float = float((vecRight.x * vecRight.x) + (vecRight.y * vecRight.y) + (vecRight.z * vecRight.z))
        vecRight.x /= length
        vecRight.y /= length
        vecRight.z /= length
        vecRight.w = 0
        return vecRight

    @staticmethod
    def cross(vecLeft, vecRight):
        nx:float = vecLeft.y * vecRight.z - vecRight.y * vecLeft.z
        ny:float = vecLeft.x * vecRight.z - vecRight.x * vecLeft.z
        nz:float = vecLeft.y * vecRight.x - vecRight.y * vecLeft.x
        nw:float = 1
        return Vector4f(nx, ny, nz, nw)
