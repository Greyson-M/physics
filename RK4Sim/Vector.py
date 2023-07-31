import math
from utils import *

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vec = [self.x, self.y]

    def __repr__(self) -> str:
        return "Vector({}, {})".format(self.x, self.y)
    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        
        raise IndexError("Vector index out of range")
    
    def tuple(self):
        return (self.x, self.y)
    
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x + other, self.y + other)
            if isinstance(other, list) or isinstance(other, tuple):
                return Vector(self.x + other[0], self.y + other[1])
            else:
                raise TypeError("Cannot add Vector to type {}".format(type(other)))
            

        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x - other, self.y - other)
            if isinstance(other, list) or isinstance(other, tuple):
                return Vector(self.x - other[0], self.y - other[1])
            else:
                raise TypeError("Cannot subtract type {} from Vector".format(type(other)))

        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x * other, self.y * other)
            if isinstance(other, list) or isinstance(other, tuple):
                return Vector(self.x * other[0], self.y * other[1])
            
            else:
                raise TypeError("Cannot multiply Vector by type {}".format(type(other)))
        
        return Vector(self.x * other.x, self.y * other.y)
    __rumul__ = __mul__
    
    def __truediv__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x / other, self.y / other)
            else:
                raise TypeError("Cannot divide Vector by type {}".format(type(other)))
        
        return Vector(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x // other, self.y // other)
            else:
                raise TypeError("Cannot divide Vector by type {}".format(type(other)))
        
        return Vector(self.x // other.x, self.y // other.y)
    
    def __mod__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x % other, self.y % other)
            else:
                raise TypeError("Cannot divide Vector by type {}".format(type(other)))
        
        return Vector(self.x % other.x, self.y % other.y)
    
    def __pow__(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, int) or isinstance(other, float):
                return Vector(self.x ** other, self.y ** other)
            else:
                raise TypeError("Cannot divide Vector by type {}".format(type(other)))
        
        return Vector(self.x ** other.x, self.y ** other.y)
    
    def __iadd__(self, other):
        if not isinstance(other, Vector):
            self.x += other
            self.y += other
        else:
            self.x += other.x
            self.y += other.y
        
        return self
    
    def __isub__(self, other):
        if not isinstance(other, Vector):
            self.x -= other
            self.y -= other
        else:
            self.x -= other.x
            self.y -= other.y
        
        return self
    
    def __imul__(self, other):
        if not isinstance(other, Vector):
            self.x *= other
            self.y *= other
        else:
            self.x *= other.x
            self.y *= other.y
        
        return self
    
    def __itruediv__(self, other):
        if not isinstance(other, Vector):
            self.x /= other
            self.y /= other
        else:
            self.x /= other.x
            self.y /= other.y
        
        return self
    
    def __ifloordiv__(self, other):
        if not isinstance(other, Vector):
            self.x //= other
            self.y //= other
        else:
            self.x //= other.x
            self.y //= other.y
        
        return self
    
    def __imod__(self, other):
        if not isinstance(other, Vector):
            self.x %= other
            self.y %= other
        else:
            self.x %= other.x
            self.y %= other.y
        
        return self
    
    def __ipow__(self, other):
        if not isinstance(other, Vector):
            self.x **= other
            self.y **= other
        else:
            self.x **= other.x
            self.y **= other.y
        
        return self
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))
    
    def __len__(self):
        return pythag(self.x, self.y)
    
    def __round__(self):
        return Vector(round(self.x), round(self.y))

    def mag(self):
        return pythag(self.x, self.y)
    magnitude = mag

    def normalize(self):
        return self/self.mag()
    normal = normalize
    unitVector = normalize

    def distance(self, other):
        if not isinstance(other, Vector):
            if isinstance(other, list) or isinstance(other, tuple):
                return pythag(self.x - other[0], self.y - other[1])
            else:
                raise TypeError("Cannot find distance between Vector and type {}".format(type(other)))

        return pythag(self.x - other.x, self.y - other.y)
    dist = distance
    distanceTo = distance

    def angle(self, other):
        return math.atan2(other.y - self.y, other.x - self.x)
    angleTo = angle

    def polar(self):
        return (self.mag(), self.angle())
    toPolar = polar
    to_polar = polar
