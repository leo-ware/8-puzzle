from itertools import product
import random


def unsparse(s):
    """sparse represenation -> grid representation"""

    # my convention is to use n for the side length of a puzzle
    # so, the 8-puzzle has n=3
    n = int(len(s) ** 0.5)

    # create the boad
    board = [[None for _ in range(n)] for _ in range(n)]

    # for each piece, ask for position, write it to the board there
    for piece, pos in s.items():
        board[pos[0]][pos[1]] = piece

    return board


def sparse(board):
    """grid representation -> sparse represenation"""
    n = len(board)
    # for each position, record that that piece was there
    return {board[i][j]: (i, j) for i, j in product(range(n), range(n))}


def flatten(l):
    """takes a 2d iterable to a 1d list
    
    example:
    [[1, 2, 3], [4, 5 ,6], [7, 8, 9]] --> [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    return [x for sublist in l for x in sublist]


def unflatten(l):
    """takes a 1d list to a 2d square array, inverse operation for flatten"""
    n = int(len(l) ** 0.5)  # errors if len(l) not an even square
    return [list(l[i * n:(i + 1) * n]) for i in range(n)]


def complete(n):
    """returns a completed puzzle of size nxn in grid form
    
    example:
    2 -->  [[0, 1], [2, 3]]
    """
    return unflatten(range(n ** 2))


def valid(state):
    """whether it is a valid board state: rows same length, all number acocunted for, no duplicates"""
    n = len(state[0])
    return ((set(flatten(state)) == set(range(n ** 2))) and  # each piece exactly once
            all(len(row) == n for row in state))  # is shaped like a square


def solvable(state):
    """finds whether the state is solveable
    
    algo from: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    """
    assert valid(state)

    n = len(state[0])
    f = flatten(state)

    # the parity of the row number where zero is... don't ask
    zero_row_parity = (f.index(0) // n) % 2 == 0

    # for the nest bit, we only want to look at pieces
    f.remove(0)

    # we're gonna look at sets of indeces i, j where i, j < n**2 and i < j
    # this is O(n^4), but thats okay because n is bounded by 4
    compare = ((i, j) for i, j in product(range(len(f)), range(len(f))) if i < j)

    # count the number of times a smaller element comes after larger elements, take parity
    swap_parity = sum(f[j] < f[i] for i, j in compare) % 2 == 0

    # aside: not *really* performance relevant, but cool to note that because I use generator comprehensions
    # rather than list comprehensions, everything is lazy, and this whole thing is actually 0(1) in memory

    # different answers for odd or even n
    if n % 2 == 1:
        return swap_parity
    else:
        return swap_parity == zero_row_parity


def m_dist(a, b):
    """manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def move(board, piece):
    """moves number 'piece' into the zero slot, returning a new state
    
    examples:
    
    [[1, 0],          [[0, 1],
     [2, 3]], 1  -->   [2, 3]]
    
    [[1, 0],          [[1, 3],
     [2, 3]], 3  -->   [2, 0]]
    """

    s = sparse(board)  # sparse fails if the board is invalid
    assert m_dist(s[piece], s[0]) == 1  # fails if the move is illegal
    s[0], s[piece] = s[piece], s[0]  # swaping pieces in sparse is easy
    return unsparse(s)


def kids(board, return_pieces=False):
    """finds all legal successor nodes to node"""

    n = len(board[0])
    s = sparse(board)

    # this is O(1) in practice because n is constant for the duration of a puzzle
    moveable = [piece for piece in flatten(board) if m_dist(s[piece], s[0]) == 1]
    moves = [move(board, m) for m in moveable]

    if return_pieces == True:
        return moves, moveable
    return moves


def scrambled(n, times=15, seed=None):
    """returns an nxn scrambled puzzle"""
    if seed:
        random.seed(seed)

    board = list(range(n ** 2))
    random.shuffle(board)
    board = unflatten(board)

    # 50% of puzzles are solvable, so this hack is fine
    if solvable(board):
        return board
    else:
        return scrambled(n, times)


def row_print(states):
    """prints a bunch of states (of the same size) on a row"""
    for row in range(len(states[0])):
        print("\t".join(str(state[row]) for state in states))


class PuzzleNode:
    """
    Class PuzzleNode: Provides a structure for performing A* search for the n^2-1 puzzle
    """

    def __init__(self, h, depth, state, parent):
        assert valid(state)
        self.h = h  # heuristic value
        self.depth = depth
        self.state = state
        self.parent = parent

    # in A*, we always expand the node with the lowest estimated distance, which is the
    # combination of the current depth of the node and the heuristic estimate of the
    # distance to the goal, the priority method here calculates that value
    @property
    def priority(self):
        return self.h + self.depth

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        # when a node is the result of an expression, you get a pretty picture in the repl
        return "\n" + "\n".join(str(row) for row in self.state)


def trace_path(root, node):
    """traces path from the root to a terminal node"""
    path = [node.state]
    while node is not root:
        node = node.parent
        path.append(node.state)
    return list(reversed(path))
