from Vector4f import *

class Matrix4f:
    mat = [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0, 0.0, 0.0, 0.0]]

    def __init__(self):
        self.mat[0][0] = 1
        self.mat[1][1] = 1
        self.mat[2][2] = 1
        self.mat[3][3] = 1

    def multiply(self, vec:Vector4f):
        newVec = \
        [
            self.mat[0][0] * vec.x + self.mat[0][1] * vec.y + self.mat[0][2] * vec.z + self.mat[0][3] * vec.w,
            self.mat[1][0] * vec.x + self.mat[1][1] * vec.y + self.mat[1][2] * vec.z + self.mat[1][3] * vec.w,
            self.mat[2][0] * vec.x + self.mat[2][1] * vec.y + self.mat[2][2] * vec.z + self.mat[2][3] * vec.w,
            self.mat[3][0] * vec.x + self.mat[3][1] * vec.y + self.mat[3][2] * vec.z + self.mat[3][3] * vec.w
        ]
        return Vector4f(newVec[0], newVec[1], newVec[2], newVec[3])

    def translate(self, trans:Vector4f):
        self.mat[0][0] = 1
        self.mat[1][1] = 1
        self.mat[2][2] = 1
        self.mat[3][3] = 1

        self.mat[0][3] = trans.x
        self.mat[1][3] = trans.y
        self.mat[2][3] = trans.z
        return self

    def screenSpaceTransform(self, width:int, height:int):
        hw:float = width / 2
        hh:float = height / 2
        self.mat[0][0] = hw
        self.mat[0][3] = hw
        self.mat[1][1] =-hh
        self.mat[1][3] = hh

        self.mat[2][2] =  1
        self.mat[3][2] = -1
        self.mat[3][3] =  0