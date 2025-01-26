from __future__ import annotations

import re
from dataclasses import dataclass
from math import isclose
from operator import indexOf

import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813


@dataclass
class DiceTest:
    dice: d
    id: str
    description: str | None = None
    repr_: str | None = None
    contents: dict | None = None
    hashed: int | None = None
    probabilities: list  | None = None
    weighted: bool | None = None
    faces: int | None = None



DiceTests = [
    DiceTest(
        dice=d(4),
        description="d4",
        repr_="Dice: d4 ({4: 1})",
        contents={4: 1},
        hashed=hash(((4,1),)),
        probabilities=[0.25, 0.25, 0.25, 0.25],
        weighted=False,
        faces=4,
        id="d4",
    ),
    DiceTest(
        dice=d(100),
        description="d100",
        repr_="Dice: d100 ({100: 1})",
        contents={100: 1},
        hashed = hash(((100,1),)),
        probabilities=[0.01] * 100,
        weighted=False,
        faces=100,
        id="d100",
    ),
    DiceTest(
        dice=2 * d(4),
        description="2d4",
        repr_="Dice: 2d4 ({4: 2})",
        contents={4: 2},
        hashed=hash(((4,2),)),
        probabilities=[0, 0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625],
        weighted=True,
        faces=8,
        id="multiplication",
    ),
    DiceTest(
        dice=d(2) + d(4),
        description="d2 + d4",
        repr_="Dice: d2 + d4 ({2: 1, 4: 1})",
        contents={2: 1, 4: 1},
        hashed=hash(((2,1),(4,1))),
        probabilities=[0, 0.125, 0.25, 0.25, 0.25, 0.125],
        weighted=True,
        faces=6,
        id="addition",
    ),
    DiceTest(
        dice=d(4) + 2,
        description="d4 + 2",
        repr_="Dice: d4 + 2 ({1: 2, 4: 1})",
        contents={1: 2, 4: 1},
        hashed=hash(((1,2),(4,1))),
        probabilities=[0, 0, 0.25, 0.25, 0.25, 0.25],
        weighted=True,
        faces=6,
        id="add constant",
    ),
    DiceTest(
        dice=d(4) + 1,
        description="d4 + 1",
        repr_="Dice: d4 + 1 ({1: 1, 4: 1})",
        contents={1: 1, 4: 1},
        hashed=hash(((1,1),(4,1))),
        probabilities=[0, 0.25, 0.25, 0.25, 0.25],
        weighted=True,
        faces=5,
        id="add 1",
    ),
    DiceTest(
        dice=d(6) + d(4),
        description="d4 + d6",
        repr_="Dice: d4 + d6 ({4: 1, 6: 1})",
        contents={4: 1, 6: 1},
        hashed=hash(((4,1),(6,1))),
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
        weighted=True,
        faces=10,
        id="unsorted addition: two dice",
    ),
    DiceTest(
        dice=(2 * d(2)) + d(4),
        description="2d2 + d4",
        repr_="Dice: 2d2 + d4 ({2: 2, 4: 1})",
        contents={2: 2, 4: 1},
        hashed=hash(((2,2),(4,1))),
        probabilities=[0, 0, 0.0625, 0.1875, 0.25, 0.25, 0.1875, 0.0625],
        weighted=True,
        faces=8,
        id="addition: complex dice",
    ),
    DiceTest(
        dice=d(4) + (2 * d(3)) + 1,
        description="2d3 + d4 + 1",
        repr_="Dice: 2d3 + d4 + 1 ({1: 1, 3: 2, 4: 1})",
        contents={1: 1, 3: 2, 4: 1},
        hashed=hash(((1,1),(3,2),(4,1))),
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
        weighted=True,
        faces=11,
        id="combined arithmetic",
    ),
    DiceTest(
        dice=d(8) + (2 * d(8)),
        description="3d8",
        repr_="Dice: 3d8 ({8: 3})",
        contents={8: 3},
        hashed=hash(((8,3),)),
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
        weighted=True,
        faces=24,
        id="add similar dice",
    ),
]


@pytest.mark.parametrize(
    ["dietype", "probabilities"],
    [pytest.param(tc.dice, tc.probabilities, id=tc.id) for tc in DiceTests if tc.probabilities is not None],
)
def test_probabilities(dietype, probabilities):
    check = [isclose(p, e) for p, e in zip(list(dietype), probabilities)]
    try:
        mismatch = indexOf(check, False)  # noqa: FBT003
        msg = f"First mismatch p({mismatch}) is {list(dietype)[mismatch]} should be {probabilities[mismatch]}"
    except ValueError:
        pass
    assert all(check), msg


@pytest.mark.parametrize(
    ["dietype", "description"],
    [pytest.param(tc.dice, tc.description, id=tc.id) for tc in DiceTests],
)
def test_str(dietype, description):
    assert str(dietype) == description

@pytest.mark.parametrize(
    ["dietype", "repr_"],
    [pytest.param(tc.dice, tc.repr_, id=tc.id) for tc in DiceTests],
)
def test_repr(dietype, repr_):
    assert repr(dietype) == repr_


@pytest.mark.parametrize(
    ["dietype", "contents"],
    [pytest.param(tc.dice, tc.contents, id=tc.id) for tc in DiceTests],
)
def test_contents(dietype, contents):
    assert dietype.contents == contents

@pytest.mark.parametrize(
    ["dietype", "hashed"],
    [pytest.param(tc.dice, tc.hashed, id=tc.id) for tc in DiceTests],
)
def test_hash(dietype, hashed):
    assert hash(dietype) == hashed

@pytest.mark.parametrize(
    ["dietype", "contents"],
    [pytest.param(tc.dice, tc.contents, id=tc.id) for tc in DiceTests],
)
def test_fromcontents(dietype: d, contents: dict):
    assert d.from_contents(contents) == dietype


@pytest.mark.parametrize(
    ["dietype", "weighted"],
    [pytest.param(tc.dice, tc.weighted, id=tc.id) for tc in DiceTests],
)
def test_weighted(dietype: d, weighted: bool):  # noqa: FBT001
    assert dietype.weighted == weighted


@pytest.mark.parametrize(
    ["dietype", "probabilities"],
    [pytest.param(tc.dice, tc.probabilities, id=tc.id) for tc in DiceTests if tc.probabilities is not None],
)
def test_first_probability(dietype, probabilities):
    assert isclose(dietype[1], probabilities[0])


@pytest.mark.parametrize(
    ["dietype", "faces"],
    [pytest.param(tc.dice, tc.faces, id=tc.id) for tc in DiceTests],
)
def test_faces(dietype: d, faces: int):
    assert len(dietype) == faces


@dataclass
class SliceTest:
    dice: d
    sides: slice
    probabilities: list
    id: str


SliceTests = [
    SliceTest(
        dice=2 * d(4),
        sides=slice(None, None),
        probabilities=[0, 0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625],
        id="full slice",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(2, 5),
        probabilities=[0.0625, 0.125, 0.1875],
        id="middle section",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(None, 5),
        probabilities=[0, 0.0625, 0.125, 0.1875],
        id="from start",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(3, None),
        probabilities=[0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625],
        id="to end",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(None, None, -1),
        probabilities=[0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625, 0],
        id="reverse full slice",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(7, 4, -1),
        probabilities=[0.125, 0.1875, 0.25],
        id="reverse middle section",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(None, 3, -1),
        probabilities=[0.0625, 0.125, 0.1875, 0.25, 0.1875],
        id="reverse from end",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(5, None, -1),
        probabilities=[0.25, 0.1875, 0.125, 0.0625, 0],
        id="reverse to start",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(2, None, 2),
        probabilities=[0.0625, 0.1875, 0.1875, 0.0625],
        id="evens",
    ),
    SliceTest(
        dice=2 * d(4),
        sides=slice(None, None, 2),
        probabilities=[0, 0.125, 0.25, 0.125],
        id="odds",
    ),
]


@pytest.mark.parametrize(
    ["dietype", "sides", "probabilities"],
    [pytest.param(tc.dice, tc.sides, tc.probabilities, id=tc.id) for tc in SliceTests],
)
def test_slicing(dietype, sides, probabilities):
    check = [isclose(p, e) for p, e in zip(dietype[sides], probabilities)]
    try:
        mismatch = indexOf(check, False)  # noqa: FBT003
        msg = f"First mismatch p({mismatch}) is {list(dietype)[mismatch]} should be {probabilities[mismatch]}"
    except ValueError:
        pass
    assert all(check), msg


def test_eq():
    d4 = d(4)
    assert d4 is not d(4)
    assert d4 == d(4)


def test_inequality():
    d4 = d(4)
    d6 = d(6)
    assert d4 != d6
    assert d4 != [None, 0.25, 0.25, 0.25, 0.25]


def test_no_sideeffects_add():
    d2 = d(2)
    adv = d2 + 1
    assert adv == d(2) + 1
    assert d2 == d(2)


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


def test_no_sideeffects_rmul():
    d4 = d(4)
    roll = 2 * d4
    assert roll == 2 * d(4)
    assert d4 == d(4)


def test_floatxDice():
    assert 2.0000001 * d(4) == 2 * d(4)


def test_stringxDice():
    assert "2" * d(4) == 2 * d(4)


def test_twoxDice():
    msg = re.escape("Cannot multiply 'two' by 'Dice'. (Hint: try using a string which only contains numbers)")
    with pytest.raises(TypeError, match=msg):
        "two" * d(4)


def test_NonexDice():
    with pytest.raises(TypeError, match="Cannot multiply 'NoneType' by 'Dice'"):
        None * d(4)


def test_index_lastside():
    assert (2 * d(4))[8] == 0.0625


def test_invalidindextype():
    with pytest.raises(TypeError, match="Cannot index 'Dice' with 'str'"):
        d(4)["two"]


def test_invalidindexvalue_too_high():
    with pytest.raises(IndexError, match="Index out of bounds, this Dice has sides numbered 1 to 4"):
        d(4)[5]


def test_invalidindexvalue_zero():
    with pytest.raises(IndexError, match="Index out of bounds, this Dice has sides numbered 1 to 4"):
        d(4)[0]


def test_cannot_change_probabilities():
    d4 = d(4)
    msg = re.escape("You cannot change a Dice's probabilities, create a new Dice instead.")
    with pytest.raises(AttributeError, match=msg):
        d4._probabilities = [1, 2]  # noqa: SLF001


def test_unpackcontents():
    die = d.from_contents({2: 1, 4: 2, 1: 3})
    assert list(die._unpackcontents()) == [[1, 2], [1, 2, 3, 4], [1, 2, 3, 4], [1], [1], [1]]  # noqa: SLF001


def test_immutable():
    d4 = d(4)
    assert d4.contents[4] == 1
    with pytest.raises(TypeError, match="Dice contents cannot be changed"):
        d4.contents[4] = 2
    assert d4.contents[4] == 1

def test_no_unwanted_mutations():
    d4 = d(4)
    assert len(d4.contents) == 1
    cached_hash = hash(d4)
    assert d4.contents[5] == 0
    assert len(d4.contents) == 1
    assert hash(d4) == cached_hash

@pytest.mark.parametrize(
    "die",
    [
        pytest.param("foo", id = "str"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(1.5, id="float"),
    ],
)
def test_invalid_dice(die):
    with pytest.raises(TypeError, match="Invalid face"):
        d(die)

@pytest.mark.parametrize(
    ["contents", "errormsg"],
    [
        pytest.param({1:"2"}, "Invalid number of Dice", id = "numdice: str"),
        pytest.param({1:-1}, "Invalid number of Dice", id = "numdice: negative"),
        pytest.param({1:2.0}, "Invalid number of Dice", id = "numdice: float"),
        pytest.param({"foo":1}, "Invalid face", id = "faces: str"),
        pytest.param({0:1}, "Invalid face", id="faces: zero"),
        pytest.param({-1:1}, "Invalid face", id="faces: negative"),
        pytest.param({1.5:1}, "Invalid face", id="faces: float"),
        # TODO Extend to cover, longer contents dicts
    ],
)
def test_invalid_from_contents(contents, errormsg):
    with pytest.raises(TypeError, match=errormsg):
        d.from_contents(contents)
