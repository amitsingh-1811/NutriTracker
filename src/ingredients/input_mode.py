from enum import Enum

class InputMode(str, Enum):
    WEIGHT = "WEIGHT"   # grams only (rice)
    COUNT = "COUNT"     # number + size (eggs)
    BOTH = "BOTH"       # banana (grams or count)