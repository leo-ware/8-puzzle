from src.heuristic_logic import _h1, _h1_cache, _h2, _h2_cache
from src.pattern_database import make_h3


# misplaced tiles
def h1(state, cache=True):
    if not cache:
        return _h1(state)
    else:
        # list is mutable -> not cacheable
        return _h1_cache(tuple(tuple(row) for row in state))


# manhattan distance
def h2(state, cache=True):
    if not cache:
        return _h2(state)
    else:
        # list is mutable -> not cacheable
        return _h2_cache(tuple(tuple(row) for row in state))


# pattern database
_h3 = make_h3()  # quite slow


def h3(state):
    return _h3(state)


heuristics = (h1, h2, h3)
