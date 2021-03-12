from src.functions import *


def test_complete():
    assert complete(2) == [[0, 1], [2, 3]]


def test_valid():
    assert valid(complete(2))
    assert not valid([[1]])


def test_solvable():
    assert not solvable([[0, 3],
                         [2, 1]])
    assert not solvable([[2, 0],
                         [1, 3]])
    assert solvable(complete(3))
    assert solvable([[1, 2, 6, 3], [0, 9, 5, 7], [4, 13, 10, 11], [8, 12, 14, 15]])


def test_move():
    assert move(move(complete(3), 1), 1) == complete(3)


def test_kids():
    assert set(kids(complete(2), return_pieces=True)[1]) == {1, 2}
    assert len(kids(complete(2))) == 2


def test_scrambled():
    assert valid(scrambled(3))
