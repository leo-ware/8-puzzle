from src.functions import *


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
