from src.node import *


def test_PuzzleNode():
    a = PuzzleNode(0, 0, [[2, 1], [3, 0]], None)
    b = PuzzleNode(0, 0, [[2, 1], [0, 3]], a)
    c = PuzzleNode(0, 0, [[0, 1], [2, 3]], b)
    path = trace_path(a, c)
    assert path == [[[2, 1], [3, 0]], [[2, 1], [0, 3]], [[0, 1], [2, 3]]]
    assert path[:][:][2] == [[0, 1], [2, 3]]

    a_ = PuzzleNode(0, 0, a.state, None)
    assert str(a) == str(a_)
