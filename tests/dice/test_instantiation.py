from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from operator import indexOf
from typing import Any

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
    probabilities: list | None = None
    weighted: bool | None = None
    faces: int | None = None


# fmt: off
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
# fmt: on


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
class InvalidContentsTestCase:
    errortype: Exception
    errormsg: str
    id: str
    contents: dict | None = None
    faces: Any | None = None


# fmt: off
invalid_contents_cases = [
    InvalidContentsTestCase(
        faces=0,
        errortype=ValueError,
        errormsg="Number of faces must be a positive integer, not 0",
        id="zero",
    ),
    InvalidContentsTestCase(
        faces=-1,
        errortype=ValueError,
        errormsg="Number of faces must be a positive integer, not -1",
        id="negative",
    ),
    InvalidContentsTestCase(
        faces="foo",
        errortype=TypeError,
        errormsg="Number of faces must be a positive integer, not str",
        id="str",
    ),
    InvalidContentsTestCase(
        faces=1.5,
        errortype=TypeError,
        errormsg="Number of faces must be a positive integer, not float",
        id="float",
    ),
    InvalidContentsTestCase(
        contents={1: "2"},
        errortype=TypeError,
        errormsg="Number of Dice must be a positive integer, not str",
        id="numdice: str",
    ),
    InvalidContentsTestCase(
        contents={1: 2.0},
        errortype=TypeError,
        errormsg="Number of Dice must be a positive integer, not float",
        id="numdice: float",
    ),
    InvalidContentsTestCase(
        contents={1: -1},
        errortype=ValueError,
        errormsg="Number of Dice must be a positive integer, not -1",
        id="numdice: negative",
    ),
    InvalidContentsTestCase(
        contents={"foo": 1},
        errortype=TypeError,
        errormsg="Number of faces must be a positive integer, not str",
        id="faces: str",
    ),
    InvalidContentsTestCase(
        contents={1.5: 1},
        errortype=TypeError,
        errormsg="Number of faces must be a positive integer, not float",
        id="faces: float",
    ),
    InvalidContentsTestCase(
        contents={0: 1},
        errortype=ValueError,
        errormsg="Number of faces must be a positive integer, not 0",
        id="faces: zero",
    ),
    InvalidContentsTestCase(
        contents={-1: 1},
        errortype=ValueError,
        errormsg="Number of faces must be a positive integer, not -1",
        id="faces: negative",
    ),
    InvalidContentsTestCase(
        contents={4: 3, 2: 3.2, 1: "2"},
        errortype=TypeError,
        errormsg="Number of Dice must be a positive integer, not str, float",
        id="numdice: partially valid types",
    ),
    InvalidContentsTestCase(
        contents={4: 3, 2: -1, 1: -2},
        errortype=ValueError,
        errormsg="Number of Dice must be a positive integer, not -2, -1",
        id="numdice: partially valid values",
    ),
    InvalidContentsTestCase(
        contents={5: 2, "-1": 1, 1: 2, 3.2: 4},
        errortype=TypeError,
        errormsg="Number of faces must be a positive integer, not float, str",
        id="faces: partially valid types",
    ),
    InvalidContentsTestCase(
        contents={5: 2, -1: 1, 1: 2, -2: 3},
        errortype=ValueError,
        errormsg="Number of faces must be a positive integer, not -2, -1",
        id="faces: partially valid values",
    ),
]
# fmt: on


@pytest.mark.parametrize(
    ["contents", "errortype", "errormsg"],
    [
        pytest.param(tc.contents, tc.errortype, tc.errormsg, id=tc.id)
        for tc in invalid_contents_cases
        if tc.contents is not None
    ],
)
def test_invalid_from_contents(contents, errortype, errormsg):
    with pytest.raises(errortype, match=errormsg):
        d.from_contents(contents)


@pytest.mark.parametrize(
    ["faces", "errortype", "errormsg"],
    [
        pytest.param(tc.faces, tc.errortype, tc.errormsg, id=tc.id)
        for tc in invalid_contents_cases
        if tc.faces is not None
    ],
)
def test_invalid_die(faces, errortype, errormsg):
    with pytest.raises(errortype, match=errormsg):
        d(faces)
