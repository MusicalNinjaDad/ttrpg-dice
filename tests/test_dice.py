import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813


def test_d4():
    d4 = d(4)
    assert d4.probabilities == [None, 0.25, 0.25, 0.25, 0.25]
    assert d4.faces == 4

def test_iterate():
    d4 = d(4)
    assert list(d4) == [0.25, 0.25, 0.25, 0.25]

def test_eq():
    d4 = d(4)
    assert d4 is not d(4)
    assert d4 == d(4)