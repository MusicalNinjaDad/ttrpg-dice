from __future__ import annotations

import re
from dataclasses import dataclass
from math import isclose
from operator import indexOf

import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813


def test_faces():
    d4 = d(4)
    assert d4.numfaces == 4
    assert list(d4.faces) == [1,2,3,4]

def test_probabilityindexes():
    die = 2 * d(4)
    assert die.probabilities[1] == 0
    assert die.probabilities[2] == 0.0625

def test_eq():
    d4 = d(4)
    assert d4 is not d(4)
    assert d4 == d(4)

def test_inequality():
    d4 = d(4)
    d6 = d(6)
    assert d4 != d6
    assert d4 != [None, 0.25, 0.25, 0.25, 0.25]

def test_add_float():
    assert d(4) + 2.0 == d(4) + 2

def test_add_string():
    assert d(4) + "2" == d(4) + 2

def test_add_two():
    msg = re.escape("Cannot add 'two' and 'Dice'. (Hint: try using a string which only contains numbers)")
    with pytest.raises(TypeError, match=msg):
        d(4) + "two"

def test_add_None():
    with pytest.raises(TypeError, match="Cannot add 'NoneType' and 'Dice'"):
        d(4) + None

def test_floatxDice():
    assert 2.0000001 * d(4) == 2*d(4)

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

def test_cannot_change_probabilities():
    d4 = d(4)
    msg = re.escape("You cannot change a Dice's probabilities, create a new Dice instead.")
    with pytest.raises(AttributeError,match=msg):
        d4.probabilities = [1,2]

def test_unpackcontents():
    contents = {2:1, 4:2, 1:3}
    assert list(d._unpackcontents(contents)) == [[1,2], [1,2,3,4], [1,2,3,4], [1], [1], [1]]  # noqa: SLF001

@dataclass
class DiceTest:
    dice: d
    description: str
    contents: dict
    probabilities: list | None
    id: str

DiceTests = [
    DiceTest(d(4), "d4", {4: 1}, [0.25, 0.25, 0.25, 0.25], id="d4"),
    DiceTest(d(100), "d100", {100: 1}, [0.01] * 100, id="d100"),
    DiceTest(2 * d(4), "2d4", {4: 2}, [0, 0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625], id="multiplication"),
    DiceTest(d(2) + d(4), "d2 + d4", {2: 1, 4: 1}, [0, 0.125, 0.25, 0.25, 0.25, 0.125], id="addition"),
    DiceTest(d(4) + 2, "d4 + 2", {1: 2, 4: 1}, [0, 0, 0.25, 0.25, 0.25, 0.25], id="add constant"),
    DiceTest(d(4) + 1, "d4 + 1", {1: 1, 4: 1}, [0, 0.25, 0.25, 0.25, 0.25], id="add 1"),
    DiceTest(
        dice=d(6) + d(4),
        description="d4 + d6",
        contents={4: 1, 6: 1},
        probabilities=[
            0,
            0.0416666666667,
            0.0833333333333,
            0.125,
            0.166666666667,
            0.166666666667,
            0.166666666667,
            0.125,
            0.0833333333333,
            0.0416666666667,
        ],
        id="unsorted addition: two dice",
    ),
    DiceTest(
        dice=(2 * d(2)) + d(4),
        description="2d2 + d4",
        contents={2: 2, 4: 1},
        probabilities=[0, 0, 0.0625, 0.1875, 0.25, 0.25, 0.1875, 0.0625],
        id="addition: complex dice",
    ),
    DiceTest(
        dice=d(4) + (2 * d(3)) + 1,
        description="2d3 + d4 + 1",
        contents={1: 1, 3: 2, 4: 1},
        probabilities=[
            0,
            0,
            0,
            0.0277777777778,
            0.0833333333333,
            0.166666666667,
            0.222222222222,
            0.222222222222,
            0.166666666667,
            0.0833333333333,
            0.0277777777778,
        ],
        id="combined arithmetic",
    ),
    DiceTest(
        dice=d(8) + (2 * d(8)),
        description="3d8",
        contents={8: 3},
        probabilities=[
            0,
            0,
            0.001953125,
            0.005859375,
            0.01171875,
            0.01953125,
            0.029296875,
            0.041015625,
            0.0546875,
            0.0703125,
            0.08203125,
            0.08984375,
            0.09375,
            0.09375,
            0.08984375,
            0.08203125,
            0.0703125,
            0.0546875,
            0.041015625,
            0.029296875,
            0.01953125,
            0.01171875,
            0.005859375,
            0.001953125,
        ],
        id="add similar dice",
    ),
]

@pytest.mark.parametrize(
    ["dietype", "probabilities"],
    [pytest.param(tc.dice, tc.probabilities, id=tc.id) for tc in DiceTests if tc.probabilities is not None],
)
def test_probabilities(dietype, probabilities):
    check = [isclose(p,e) for p, e in zip(list(dietype), probabilities)]
    try:
        mismatch = indexOf(check, False)  # noqa: FBT003
        msg = f"First mismatch p({mismatch}) is {list(dietype)[mismatch]} should be {probabilities[mismatch]}"
    except ValueError: pass
    assert all(check), msg

@pytest.mark.parametrize(
    ["dietype", "description"],
    [pytest.param(tc.dice, tc.description, id=tc.id) for tc in DiceTests],
)
def test_str(dietype, description):
    assert str(dietype) == description

@pytest.mark.parametrize(
    ["dietype", "contents"],
    [pytest.param(tc.dice, tc.contents, id=tc.id) for tc in DiceTests],
)
def test_contents(dietype, contents):
    assert dietype.contents == contents

@pytest.mark.parametrize(
    ["dietype", "contents"],
    [pytest.param(tc.dice, tc.contents, id=tc.id) for tc in DiceTests],
)
def test_fromcontents(dietype: d, contents: dict):
    assert d.from_contents(contents) == dietype
