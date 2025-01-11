import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813


def test_d4():
    d4 = d(4)
    assert d4.probabilities == [None, 0.25, 0.25, 0.25, 0.25]
    assert d4.numfaces == 4

def test_iterate():
    d4 = d(4)
    assert list(d4) == [0.25, 0.25, 0.25, 0.25]

def test_eq():
    d4 = d(4)
    assert d4 is not d(4)
    assert d4 == d(4)

def test_inequality():
    d4 = d(4)
    d6 = d(6)
    assert d4 != d6
    assert d4 != [None, 0.25, 0.25, 0.25, 0.25]

def test_from_probabilities():
    d4 = d.from_probabilities([None, 0.25, 0.25, 0.25, 0.25])
    assert d4 == d(4)

def test_iterate_faces():
    d4 = d(4)
    assert list(d4.faces) == [1,2,3,4]

def test_2d4():
    assert (2 * d(4)).probabilities == [None, 0, 0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625]