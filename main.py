import enum


class STACK(enum.StrEnum):
    STANDARD = "standard"
    SPECIAL = "special"
    REJECTED = "rejected"


"""
Thresholds are inclusive
"""
BULKY_VOLUME_THRESHOLD_CM3 = 1000000
BULKY_DIMENSION_THRESHOLD_CM = 150
HEAVY_THRESHOLD_KG = 20



def is_bulky(width: int, height: int , length: int) -> bool:
    return max(width, height, length) >= BULKY_DIMENSION_THRESHOLD_CM  or (width*height*length >= BULKY_VOLUME_THRESHOLD_CM3)

def is_heavy(weight: int) -> bool:
    return weight >= HEAVY_THRESHOLD_KG


def sort(width: int, height: int, length: int, mass: int) -> STACK:
    heavy = is_heavy(mass)
    bulky = is_bulky(width,height,length)
    if heavy and bulky:
        return STACK.REJECTED
    if heavy or bulky:
        return STACK.SPECIAL

    return STACK.STANDARD



