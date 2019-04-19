import random
import math

def random_bump(val, minval, maxval, maxBump):

    bump_direction = (random.random()-0.5)*2 * maxBump # (-0.5 to 0.5)*2 * maxBump makes a bump in either direction by an amount less than maxBump

    return clamp(val+bump_direction, minval, maxval)


def clamp(val, minval, maxval):
    return min(max(val, minval), maxval)

def sind(degrees):
    return math.sin(math.radians(degrees))

def cosd(degrees):
    return math.cos(math.radians(degrees))