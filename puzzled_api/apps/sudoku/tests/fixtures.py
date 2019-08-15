import pytest


@pytest.fixture(scope='module')
def puzzle():
    return [[5, 7, 0, 0, 0, 0, 3, 0, 0],
             [0, 4, 0, 0, 5, 3, 9, 0, 0],
             [9, 0, 0, 0, 0, 8, 0, 0, 0],

             [0, 0, 6, 5, 0, 0, 0, 0, 4],
             [3, 0, 0, 6, 4, 9, 0, 0, 0],
             [4, 0, 5, 0, 0, 0, 0, 6, 0],

             [0, 0, 0, 1, 0, 5, 2, 0, 0],
             [0, 5, 0, 0, 0, 0, 7, 0, 0],
             [0, 0, 0, 0, 7, 0, 0, 5, 1]]


@pytest.fixture(scope='module')
def invalid_puzzle():
    return [[5, 7, 0, 0, 0, 0, 3, 0, 0],
            [0, 4, 0, 0, 5, 3, 9, 0, 0],
            [9, 0, 7, 0, 0, 8, 0, 0, 0],

            [0, 0, 6, 5, 0, 0, 0, 0, 4],
            [3, 0, 0, 6, 4, 9, 0, 4, 0],
            [4, 0, 5, 0, 9, 0, 0, 6, 0],

            [0, 0, 0, 1, 0, 5, 2, 0, 5],
            [0, 5, 0, 0, 0, 0, 7, 5, 0],
            [9, 0, 0, 0, 7, 0, 0, 5, 1]]
