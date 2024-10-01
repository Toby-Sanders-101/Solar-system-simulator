import math
from typing import Self, List
from vectors import *

class Matrix:
    def __init__(self, values):
        self.values = values
        self.rows = len(values)
        self.cols = len(values[0])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Matrix A's columns must equal Matrix B's rows")

            arr = [[0 for c in range(other.cols)] for r in range(self.rows)]
            for y in range(self.rows):
                for col in range(other.cols):
                    for x in range(self.cols):
                        arr[y][col] += self.values[y][x] * other.values[x][col]
            return Matrix(arr)
        else:
            return NotImplemented

    def __repr__(self):
        return f"Matrix({self.values})"
    
    @property
    def asVector3(self):
        if self.cols == 1 and self.rows == 3:
            return Vector3(self.values[0][0], self.values[1][0], self.values[2][0])

def multiply(*args):
    l = len(args)
    for i in range(l):
        m = args[l-i-1]
        if isinstance(m, Matrix):
            pass
        elif isinstance(m, Vector):
            if isinstance(m, Vector2):
                m = Matrix([[m.x],[m.y]])
            
            elif isinstance(m, Vector3):
                m = Matrix([[m.x],[m.y],[m.z]])
        else:
            raise Exception("unknown type",type(m))
        if i==0:
            matrix = m
        else:
            matrix = m * matrix
    return matrix

class rotationmatrix3x3(Matrix):
    def __init__(self, axis, angle):
        rads = math.radians(angle)
        cos = math.cos(rads)
        sin = math.sin(rads)
        if axis == 'x':
            arr = [[   1,   0,   0],\
                   [   0, cos,-sin],\
                   [   0, sin, cos]]
        elif axis == 'y':
            arr = [[ cos,   0, sin],\
                   [   0,   1,   0],\
                   [-sin,   0, cos]]
        elif axis == 'z':
            arr = [[ cos,-sin,   0],\
                   [ sin, cos,   0],\
                   [   0,   0,   1]]
        else:
            raise Exception("unknown axis",axis)
        super().__init__(arr)

# a = Matrix([[1,0,0],[0,1,0],[0,0,1]])
# a = rotationmatrix3x3("x",90)
# b = Matrix([[1,2,3],[4,5,6],[7,8,9]])
# c = Vector3(10, 100, 1000)

# multiply(a, b)
# multiply(a, c)
# multiply(b, a)
# multiply(b, a, c)