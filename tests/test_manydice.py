import pytest  # noqa: F401, RUF100

from ttrpg_dice.manydice import _p, multiroll


@pytest.mark.xfail # NotImplemented
def test_2d100_target33():
    assert multiroll(2, 100, 33) == [100, 55, 11]

def test_2d100_target33_p1hit():
    assert _p(2, 100, 33, 1) == 44

def test_2d100_target33_p2hit():
    assert _p(2, 100, 33, 2) == 11