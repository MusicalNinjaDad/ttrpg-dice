import re
from dataclasses import dataclass

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
    d4 = d.from_probabilities([None, 0.25, 0.25, 0.25, 0.25], "")
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

def test_invalidprobs_p0_not_None():
    msg = re.escape("First probability, P(0), must be `None`")
    with pytest.raises(ValueError, match=msg):
        d.from_probabilities([0.5,0.5], "")

def test_invalidprobs_px_is_None():
    msg = re.escape("Only the first probability, P(0), may be `None`")
    with pytest.raises(ValueError, match=msg):
        d.from_probabilities([None, 0.5, 0.5, None], "")

def test_cannot_change_probabilities():
    d4 = d(4)
    msg = re.escape("You cannot change a Dice's probabilities, create a new Dice instead.")
    with pytest.raises(AttributeError,match=msg):
        d4.probabilities = [1,2]

def test_does_not_sum_to_1():
    msg = re.escape("Dice probabilities must sum to 1 (not 2.0)")
    with pytest.raises(ValueError,match=msg):
        d.from_probabilities([None, 0.5, 1.5], "")

@dataclass
class ArithmeticTest:
    dice: d
    description: str
    contents: dict
    id: str

ArithmeticCases = [
    ArithmeticTest(d(100), "d100", {100:1}, id="d100"),
    ArithmeticTest(2 * d(4), "2d4", {4:2}, id="2d4"),
    ArithmeticTest(d(4) + d(6), "d4 + d6", {4:1, 6:1}, id="d4 + d6"),
    ArithmeticTest(d(8) + 5, "d8 + 5", {1:5, 8:1}, id="d8 + 5"),
    ArithmeticTest(d(6) + d(4), "d4 + d6", {4:1, 6:1}, id="sorting addition: two dice"),
    ArithmeticTest(d(6) + (2 * d(4)), "2d4 + d6", {4:2,6:1}, id="sorting addition: complex dice"),
    ArithmeticTest((2 * d(6)) + d(8) + 5, "2d6 + d8 + 5", {1:5, 6:2, 8:1}, id="combined arithmetic"),
    ArithmeticTest(d(8) + (2 * d(8)), "3d8", {8:3}, id="add similar dice"),
]


@pytest.mark.parametrize(
    ["dietype", "description"],
    [pytest.param(tc.dice, tc.description, id=tc.id) for tc in ArithmeticCases],
)
def test_str(dietype, description):
    assert str(dietype) == description

@pytest.mark.parametrize(
    ["dietype", "contents"],
    [pytest.param(tc.dice, tc.contents, id=tc.id) for tc in ArithmeticCases],
)
def test_contents(dietype, contents):
    assert dietype.contents == contents


@pytest.mark.parametrize(
    ["contents", "description"],
    [pytest.param(tc.contents, tc.description, id=tc.id) for tc in ArithmeticCases],
)
def test_describe(contents, description):
    assert d.describe(contents) ==  description