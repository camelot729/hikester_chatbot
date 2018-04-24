from enum import Enum

class State(Enum):
    HI_SECTION = 'hi'
    BYE_SECTION = 'bye'
    TIME_SECTION = 'time'
    PLACE_SECTION = 'place'
    COST_SECTION = 'cost'
    EMPTY_SECTION = 'empty'
    FACT_SECTION = 'fact'