from src.functions import *
from functools import lru_cache


# Misplaced tiles heuristic
def _h1(state):
    """
    This function returns the number of misplaced tiles, given the board state
    Input:
        -state: the board state as a list of lists
    Output:
        -h: the number of misplaced tiles
    """
    # counts the spaces where the current and completed boards differ
    return sum((i != j) and (0 != j) for i, j in zip(flatten(complete(len(state))), flatten(state)))


# cached version
@lru_cache
def _h1_cache(state):
    return _h1(state)


def _h2(state):
    """
    This function returns the Manhattan distance from the solved state, given the board state
    Input:
        -state: the board state as a list of lists
    Output:
        -h: the Manhattan distance from the solved configuration
    """
    c = sparse(complete(len(state)))
    s = sparse(state)

    # sums the manhattan distance between positions in the current and completed board
    # for each piece ignoring zero
    return sum(m_dist(s[piece], c[piece]) for piece in range(len(state) ** 2) if piece != 0)


# cached version
@lru_cache
def _h2_cache(state):
    return _h2(state)
