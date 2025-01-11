import re

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

def test_floatxDice():
    assert (2.0000001 * d(4)).probabilities == [None, 0, 0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625]

def test_stringxDice():
    assert "2" * d(4) == 2 * d(4)

def test_twoxDice():
    msg = re.escape("Cannot multiply 'two' by 'Dice'. (Hint: try using a string which only contains numbers)")
    with pytest.raises(TypeError, match=msg):
        "two" * d(4)

def test_NonexDice():
    with pytest.raises(TypeError, match="Cannot multiply 'NoneType' by 'Dice'"):
        None * d(4)

def test_weighted():
    assert (2 * d(4)).weighted

def test_notweighted():
    assert not d(4).weighted

def test_d4_plus_d2():
    mix = d(4) + d(2)
    assert list(mix) == [0, 0.125, 0.25, 0.25, 0.25, 0.125]

def test_d4_plus_2():
    advantage = d(4) + 2
    assert list(advantage) == [0, 0, 0.25, 0.25, 0.25, 0.25]

def test_d4_plus_float():
    advantage = d(4) + 2.0
    assert list(advantage) == [0, 0, 0.25, 0.25, 0.25, 0.25]

def test_Dice_plus_string():
    assert d(4) + "2" == d(4) + 2

def test_Dice_plus_two():
    msg = re.escape("Cannot add 'two' and 'Dice'. (Hint: try using a string which only contains numbers)")
    with pytest.raises(TypeError, match=msg):
        d(4) + "two"

def test_Dice_plus_None():
    with pytest.raises(TypeError, match="Cannot add 'NoneType' and 'Dice'"):
        d(4) + None

def test_d4x2():
    advantage = d(4) * 2
    assert list(advantage) == [0, 0.25, 0, 0.25, 0, 0.25, 0, 0.25]