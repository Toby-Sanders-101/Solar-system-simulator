import numpy as np
from typing import Self

class Vector:
    pass

class Vector2(Vector):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, b: Self) -> Self:
        return Vector2(self.x+b.x, self.y+b.y)
    
    def __sub__(self, b: Self) -> Self:
        return Vector2(self.x-b.x, self.y-b.y)
    
    def __mul__(self, k: float) -> Self:
        return Vector2(self.x * k, self.y * k)
    
    def __truediv__(self, k: float) -> Self:
        return Vector2(self.x / k, self.y / k)
    
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    
    @property
    def mag(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)

    @property
    def norm(self) -> Self:
        return self / self.mag
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y)

class Vector3(Vector):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, b: Self) -> Self:
        return Vector3(self.x+b.x, self.y+b.y, self.z+b.z)
    
    def __sub__(self, b: Self) -> Self:
        return Vector3(self.x-b.x, self.y-b.y, self.z-b.z)
    
    def __mul__(self, k: float) -> Self:
        return Vector3(self.x * k, self.y * k, self.z * k)
    
    def __truediv__(self, k: float) -> Self:
        return Vector3(self.x / k, self.y / k, self.z / k)

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    @property
    def mag(self) -> float:
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    @property
    def norm(self) -> Self:
        return self / self.mag
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y, self.z)
    
    @property
    def asVector2(self) -> Vector2:
        return Vector2(self.x, self.y)