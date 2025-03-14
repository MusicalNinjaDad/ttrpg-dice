from __future__ import annotations

import re
from dataclasses import dataclass
from math import isclose
from operator import indexOf

import pytest  # noqa: F401, RUF100


@dataclass
class SliceTest:
    id: str
    index: slice | int
    dice_expr: str
    probabilities: list | None = None
    errortype: Exception | None = None
    errormsg: str | None = None


# fmt: off
SliceTests = [
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(None, None),
        probabilities=[0, 0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625],
        id="full slice",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(2, 5),
        probabilities=[0.0625, 0.125, 0.1875],
        id="middle section",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(None, 5),
        probabilities=[0, 0.0625, 0.125, 0.1875],
        id="from start",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(3, None),
        probabilities=[0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625],
        id="to end",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(None, None, -1),
        probabilities=[0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625, 0],
        id="reverse full slice",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(-1, 0, -1),
        probabilities=[0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625, 0],
        id="reverse full slice to zero",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(None, 1, -1),
        probabilities=[0.0625, 0.125, 0.1875, 0.25, 0.1875, 0.125, 0.0625, 0],
        id="reverse slice to 2",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(7, 4, -1),
        probabilities=[0.125, 0.1875, 0.25],
        id="reverse middle section",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(None, 3, -1),
        probabilities=[0.0625, 0.125, 0.1875, 0.25, 0.1875],
        id="reverse from end",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(5, None, -1),
        probabilities=[0.25, 0.1875, 0.125, 0.0625, 0],
        id="reverse to start",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(2, None, 2),
        probabilities=[0.0625, 0.1875, 0.1875, 0.0625],
        id="explicit evens",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(None, None, 2),
        probabilities=[0.0625, 0.1875, 0.1875, 0.0625],
        id="implicit evens",
    ),
    SliceTest(
        dice_expr="2 * d(4)",
        index=slice(1, None, 2),
        probabilities=[0, 0.125, 0.25, 0.125],
        id="odds",
    ),
]
# fmt: on


@pytest.mark.parametrize(
    ["dietype", "sides", "probabilities"],
    [pytest.param(tc.dice_expr, tc.index, tc.probabilities, id=tc.id) for tc in SliceTests],
    indirect=["dietype"],
)
def test_slicing(dietype, sides, probabilities):
    check = [isclose(p, e) for p, e in zip(dietype[sides], probabilities)]  # noqa: B905
    try:
        mismatch = indexOf(check, False)  # noqa: FBT003
        msg = f"First mismatch p({mismatch}) is {list(dietype)[mismatch]} should be {probabilities[mismatch]}"
    except ValueError:
        pass
    assert all(check), msg


# fmt: off
IndexTests = [
    SliceTest(
        id="1",
        dice_expr="2 * d(4)",
        index=1,
        probabilities=0,
    ),
    SliceTest(
        id="2",
        dice_expr="2 * d(4)",
        index=2,
        probabilities=0.0625,
    ),
    SliceTest(
        id="-1",
        dice_expr="2 * d(4)",
        index=-1,
        probabilities=0.0625,
    ),
    SliceTest(
        id="-2",
        dice_expr="2 * d(4)",
        index=-2,
        probabilities=0.125,
    ),
    SliceTest(
        id="8 of 8",
        dice_expr="2 * d(4)",
        index=8,
        probabilities=0.0625,
    ),
    SliceTest(
        id="-8 of 8",
        dice_expr="2 * d(4)",
        index=-8,
        probabilities=0,
    ),
]
# fmt: on


@pytest.mark.parametrize(
    ["dietype", "side", "probability"],
    [pytest.param(tc.dice_expr, tc.index, tc.probabilities, id=tc.id) for tc in IndexTests],
    indirect=["dietype"],
)
def test_indexing(dietype, side, probability):
    assert dietype[side] == pytest.approx(probability)


# fmt: off
InvalidIndexTests = [
    SliceTest(
        id="zero",
        index=0,
        dice_expr="d(10)",
        errortype=IndexError,
        errormsg="Invalid side: This Dice has sides numbered 1 to 10.",
    ),
    SliceTest(
        id="too high",
        index=11,
        dice_expr="d(10)",
        errortype=IndexError,
        errormsg="Invalid side: This Dice has sides numbered 1 to 10.",
    ),
    SliceTest(
        id="negative results in p(0)",
        index=-11,
        dice_expr="d(10)",
        errortype=IndexError,
        errormsg="Invalid side: This Dice has sides numbered 1 to 10.",
    ),
    SliceTest(
        id="too big negative",
        index=-12,
        dice_expr="d(10)",
        errortype=IndexError,
        errormsg="Invalid side: This Dice has sides numbered 1 to 10.",
    ),
    SliceTest(
        id="number as string",
        index="3",
        dice_expr="d(10)",
        errortype=TypeError,
        errormsg="Cannot index 'Dice' with 'str'.",
    ),
    SliceTest(
        id="slice from zero",
        index=slice(0, None, None),
        dice_expr="d(10)",
        errortype=IndexError,
        errormsg="Invalid side: This Dice has sides numbered 1 to 10.",
    ),
]
# fmt: on


@pytest.mark.parametrize(
    ["dietype", "index", "errortype", "errormsg"],
    [pytest.param(tc.dice_expr, tc.index, tc.errortype, tc.errormsg, id=tc.id) for tc in InvalidIndexTests],
    indirect=["dietype"],
)
def test_invalid_index(dietype, index, errortype, errormsg):
    msg = re.escape(errormsg)
    with pytest.raises(errortype, match=msg):
        dietype[index]
