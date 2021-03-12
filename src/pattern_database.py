from src.functions import *
from collections import deque


def make_abstractor(rule):
    """Takes a rule determining which numbers to blot out and returns a mapping from problems to abstract problems
    """

    def keep(piece):
        return isinstance(piece, int) and (rule(piece) or piece == 0)

    def abstract(board):
        return str(unflatten([i if keep(i) else "*" for i in flatten(board)]))

    return abstract


assert make_abstractor(lambda x: x == 2)(complete(2)) == "[[0, '*'], [2, '*']]"


def concrete(board_str):
    """Takes an abstract problem and returns a concrete problem belonging to the corresponding equivalence class
    """
    counter = 1
    new = []
    for item in flatten(eval(board_str)):
        if item == "*":
            new.append("*" + str(counter))
            counter += 1
        else:
            new.append(item)
    return unflatten(new)


def dezero(s):
    return s.replace("0", "'*'")


def make_db(n, rule):
    abstract = make_abstractor(rule)
    db = {}
    seen = set()
    queue = deque([(abstract(complete(n)), 0)])

    # start bfs
    while queue:
        node, node_depth = queue.pop()

        # calculate children and iterate over them
        for kid_board, piece_moved in zip(*kids(concrete(node), return_pieces=True)):

            kid_abs_board = abstract(kid_board)  # map board into an abstract space
            is_relevant_move = (not isinstance(piece_moved, str) and rule(piece_moved))
            kid_depth = node_depth + is_relevant_move  # only increments depth if the pieece moved was relevent

            # tree nodes count as different if the zero is in a different place
            if kid_abs_board in seen:
                continue
            seen.add(kid_abs_board)

            # if we haven't seen this node before, add it to db with its depth
            # simplified states do not count as different if zero is in a different place
            if dezero(kid_abs_board) not in db:
                db[dezero(kid_abs_board)] = kid_depth

            queue.appendleft((kid_abs_board, kid_depth))

    # key function used to access dictionary items
    def key(board):
        return dezero(abstract(board))

    return db, key


def odd(i):
    return i % 2 == 1


def even(i):
    return i % 2 == 0


def create_pattern_databases(ns):
    # map from puzzle size to relevant heuristic function
    dbs = {}

    # create heuristic functions of desired sizes
    for n in ns:
        odd_db, odd_key = make_db(n, odd)
        even_db, even_key = make_db(n, even)

        def heuristic(state):
            return odd_db[odd_key(state)] + even_db[even_key(state)]

        dbs[n] = heuristic

    return dbs


def make_h3(ns=(2, 3)):
    _dbs = create_pattern_databases(ns)

    def _h3(state):
        """
        This function returns a heuristic that dominates the Manhattan distance, given the board state
        Input:
            -state: the board state as a list of lists
        Output:
            -h: the Heuristic distance of the state from its solved configuration
        """
        # figure out db size
        n = len(state[0])

        # looks up the appropriate heuristic and uses it to evaluate the state
        # fails with KeyError when the heuristic has not been generated
        return _dbs[n](state)

    return _h3
