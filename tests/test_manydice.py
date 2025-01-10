import pytest  # noqa: F401, RUF100

from ttrpg_dice import lazyroll


def test_2d100_target33():
    assert lazyroll(2, 100, 33) == [100, 55, 11]

def test_5d100_target33_haszeroresult():
    assert lazyroll(5, 100, 33) == [100, 86, 53, 20, 4, 0]

def test_3d100_target41_roundingto100():
    assert lazyroll(3, 100, 41) == [100, 79, 37, 7]

def test_2d4_target2():
    assert lazyroll(2, 4, 2) == [4, 3, 1]