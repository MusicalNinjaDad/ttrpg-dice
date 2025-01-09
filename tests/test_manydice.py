import pytest  # noqa: F401, RUF100

from ttrpg_dice.manydice import multiroll


def test_2d100_target33():
    assert multiroll(2, 100, 33) == [100, 55, 11]