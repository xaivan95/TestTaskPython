from enum import Enum

class FormatterType(Enum):
    RAW = "raw"
    NORMAL = "NORMAL"
    DELTA = "delta"

class TimeConstants:
    MS_IN_SECOND = 1000
    DEFAULT_SERIES_SIZE = 5