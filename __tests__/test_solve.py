from src.solve import *
from src.heuristics import heuristics


def test_solve_puzzle():
    incorrect_state = [[0, 1, 2], [2, 3, 4], [5, 6, 7]]
    _, _, _, _, err = solve_puzzle(incorrect_state, lambda state: 0)
    assert (err == -1)


def test_catches_unsolvable():
    unsolvable_initial_state = [[7, 5, 6], [2, 4, 3], [8, 1, 0]]
    _, _, _, _, err = solve_puzzle(unsolvable_initial_state, lambda state: 0)
    assert (err == -2)


def test_heuristics_sam():
    working_initial_states_8_puzzle = (
    [[2, 3, 7], [1, 8, 0], [6, 5, 4]], [[7, 0, 8], [4, 6, 1], [5, 3, 2]], [[5, 7, 6], [2, 4, 3], [8, 1, 0]])
    opt_path_soln = [[[2, 3, 7], [1, 8, 0], [6, 5, 4]], [[2, 3, 7], [1, 8, 4], [6, 5, 0]],
                     [[2, 3, 7], [1, 8, 4], [6, 0, 5]], [[2, 3, 7], [1, 0, 4], [6, 8, 5]],
                     [[2, 0, 7], [1, 3, 4], [6, 8, 5]], [[0, 2, 7], [1, 3, 4], [6, 8, 5]],
                     [[1, 2, 7], [0, 3, 4], [6, 8, 5]], [[1, 2, 7], [3, 0, 4], [6, 8, 5]],
                     [[1, 2, 7], [3, 4, 0], [6, 8, 5]], [[1, 2, 0], [3, 4, 7], [6, 8, 5]],
                     [[1, 0, 2], [3, 4, 7], [6, 8, 5]], [[1, 4, 2], [3, 0, 7], [6, 8, 5]],
                     [[1, 4, 2], [3, 7, 0], [6, 8, 5]], [[1, 4, 2], [3, 7, 5], [6, 8, 0]],
                     [[1, 4, 2], [3, 7, 5], [6, 0, 8]], [[1, 4, 2], [3, 0, 5], [6, 7, 8]],
                     [[1, 0, 2], [3, 4, 5], [6, 7, 8]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]

    astar_steps = [17, 25, 28]

    for i in range(0, 3):
        steps_mt, expansions_mt, _, opt_path_mt, _ = solve_puzzle(working_initial_states_8_puzzle[i], heuristics[0])
        steps_man, expansions_man, _, opt_path_man, _ = solve_puzzle(working_initial_states_8_puzzle[i], heuristics[1])

        # Test whether the number of optimal steps is correct and the same
        assert (steps_mt == steps_man == astar_steps[i])

        # Test whether or not the manhattan distance dominates the misplaced tiles heuristic in every case
        assert (expansions_man < expansions_mt)

        # For the first state, test that the optimal path is the same
        if i == 0:
            assert (opt_path_mt == opt_path_soln)
