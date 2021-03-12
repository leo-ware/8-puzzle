from src.heapy import MinHeap
from src.functions import *


# main solvePuzzle function.
def solve_puzzle(state, heuristic):
    """This function should solve the n**2-1 puzzle for any n > 2 (although it may take too long for n > 4)).
    Inputs:
        -state: The initial state of the puzzle as a list of lists
        -heuristic: a handle to a heuristic function.  Will be one of those defined in Question 2.
    Outputs:
        -steps: The number of steps to optimally solve the puzzle (excluding the initial state)
        -exp: The number of nodes expanded to reach the solution
        -max_frontier: The maximum size of the frontier over the whole search
        -opt_path: The optimal path as a list of list of lists.  That is, opt_path[:,:,i] should give a list of lists
                    that represents the state of the board at the ith step of the solution.
        -err: An error code.  If state is not of the appropriate size and dimension, return -1.  For the extention task,
          if the state is not solvable, then return -2
    """

    if not valid(state):
        print("invalid!")
        return 0, 0, 0, None, -1

    if not solvable(state):
        print('unsolvable!')
        return 0, 0, 0, None, -2

    n = len(state)  # an nxn board
    h = heuristic  # function: state -> score
    goal = complete(n)  # creates a completed nxn puzzle for comparison
    visited = set()

    # edge case when we are fed a completed puzzle
    if state == goal:
        return 0, 0, 1, [state], 0

    # things we have to track
    exp = 0
    max_front = 1

    # initial search state
    root = PuzzleNode(h=h(state), depth=0, state=state, parent=None)
    queue = MinHeap()
    queue.push(root, root.priority)

    while not queue.empty:

        exp += 1  # we're expanding a node, so increment count of nodes we have expanded
        max_front = max(max_front, len(queue))  # the queue is the frontier

        # take the most promising node and expand it
        node = queue.pop()

        for kid in kids(node.state):

            # this is graph search, so i maintiain a hash set of visited
            # states and do not revisit them
            if str(kid) in visited:
                continue
            else:
                visited.add(str(kid))

            # construct a node from a state
            kid_node = PuzzleNode(
                h=h(kid),  # heursitic value of state
                depth=node.depth + 1,  # distance from root
                state=kid,  # state in grid form
                parent=node  # remember parent for retracing
            )

            # check if this is the goal node
            if kid == goal:
                path = trace_path(root, kid_node)
                return len(path) - 1, exp, max_front, path, 0
            else:
                queue.push(kid_node, kid_node.priority)
