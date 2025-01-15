import pytest  # noqa: F401, RUF100

from ttrpg_dice import LazyRollTable, lazyroll


def test_2d100_target33():
    assert lazyroll(2, 100, 33) == [100, 55, 11]

def test_5d100_target33_haszeroresult():
    assert lazyroll(5, 100, 33) == [100, 86, 53, 20, 4, 0]

def test_3d100_target41_roundingto100():
    assert lazyroll(3, 100, 41) == [100, 79, 37, 7]

def test_2d4_target2():
    assert lazyroll(2, 4, 2) == [4, 3, 1]

def test_0d100():
    assert lazyroll(0, 100, 33) == [100]

def test_guaranteedhit():
    assert lazyroll(3,20,20) == [20, 20, 20, 20]

def test_guaranteedfail():
    with pytest.raises(ValueError,match="Good luck rolling 13 on a d12!"):
        lazyroll(3, 12, 13)

def test_guaranteedfail_LazyTable():
    with pytest.raises(ValueError,match="Good luck rolling 13 on a d12!"):
        LazyRollTable(3, 12, 13)

def test_lazytable_eq_lazytable():
    assert LazyRollTable(4, 100, 33) == LazyRollTable(4, 100, 33)

def test_lazytable_upto4d100_target33():
    assert LazyRollTable(4, 100, 33) == [
        [100],
        [100, 33],
        [100, 55, 11],
        [100, 70, 25, 4],
        [100, 80, 40, 11, 1],
    ]

def test_lazytable_upto4d100_target33_pretty():
    output = r"""Lazyroll table for up to 4d100 targeting 33 for success:

	HITS
	1	2	3	4
1	33
2	55	11
3	70	25	4
4	80	40	11	1"""
    assert str(LazyRollTable(4, 100, 33)) == output
