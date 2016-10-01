#Common 2d vector function apply to tupples
from math import sqrt

class Vect:
    def __init__((x,y)):
        self.x = x
        self.y = y
    def tple(self):
        """Return a tuple representing the vect"""
        return (self.x,self.y)
    

def suma(p1,p2):
    """Suma de dos vectores p1 y p2"""
    if type(p1) != tuple or type(p2) != tuple:
        raise TypeError('Is not tuple',p1,p2)
    if len(p1) != 2 or len(p2) != 2:
        raise ValueError ('tupple lenght different from 2',p1,p2)
    x = p1[0]+p2[0]
    y = p1[1]+p2[1]

    return (x,y)
def div(v,n):
    return (v[0]/n,v[1]/n)
def modulo(v):
    return sqrt(v[0]*v[0]+v[1]*v[1])
def dist(p1,p2):
    """Distancia entre dos puntos"""
    return modulo((p1[0]-p2[0],p1[1]-p2[1]))
def isInsideRect(v,rect):
    """is the point v inside the rect ( 0,0,rect.x,rect.y)"""
    return v[0] < rect[0] and v[0]>= 0 and v[1] < rect[1] and v[1] >= 0
def inverse(v):
    return (v[0]*(-1),v[1]*(-1))
def resta(p1,p2):
    return suma(p1,inverse(p2))


if __name__ == '__main__':
    p1 = (1,1)
    p2 = (2,2)

    print dist(p1,p2)
