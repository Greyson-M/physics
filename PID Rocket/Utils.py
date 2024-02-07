import math

#UTILIY FUNCTIONS
def pythag (vector):
    return math.sqrt((vector[0]**2) + (vector[1]**2))

def distance (vec1, vec2):
    xdis = vec2[0] - vec1[0]
    ydis = vec2[1] - vec1[1]
    return pythag([xdis, ydis])

def E(x):
        return 10**x