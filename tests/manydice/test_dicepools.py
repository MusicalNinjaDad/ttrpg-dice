from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813
from ttrpg_dice.manydice import PoolComparison

# Anydice calculation:
# function: range on DIE:n between LOW:n and HIGH:n {
# if DIE >= LOW & DIE <= HIGH { result: 1 }
# result: 0
# }

# POOL: 2d4

# output [range on POOL between 1 and 4]
# output [range on POOL between 5 and 6]
# output [range on POOL between 7 and 8]


@dataclass
class PoolTestCase:
    pools: dict[Any, d] | list[d]
    poolsdict: dict[Any, d]
    outcomes: dict[Any, slice]
    chances: dict[tuple[Any, Any], float]
    table: str
    plotabledata: dict[str, list]


# fmt: off
namedpools = PoolTestCase(
    pools={
        "two dice plus": (2*d(3)) + 2,
        "two dice": 2*d(4),
        "one dice plus": d(6)+2,
        "one dice": d(8),
    },
    poolsdict={
        "two dice plus": (2*d(3)) + 2,
        "two dice": 2*d(4),
        "one dice plus": d(6)+2,
        "one dice": d(8),
    },
    outcomes={
        "under 4": slice(None, 5),
        "5 or 6": slice(5,7),
        "over 6": slice(7,None),
    },
    chances = {
        ("two dice plus", "under 4"): 0.111111111111,
        ("two dice plus", "5 or 6"): 0.555555555556,
        ("two dice plus", "over 6"): 0.333333333333,
        ("two dice", "under 4"): 0.375,
        ("two dice", "5 or 6"): 0.4375,
        ("two dice", "over 6"): 0.1875,
        ("one dice plus", "under 4"): 0.33333333333,
        ("one dice plus", "5 or 6"): 0.33333333333,
        ("one dice plus", "over 6"): 0.33333333333,
        ("one dice", "under 4"): 0.5,
        ("one dice", "5 or 6"): 0.25,
        ("one dice", "over 6"): 0.25,
    },
    table = """\
pool             under 4    5 or 6    over 6
two dice plus      11.11     55.56     33.33
two dice           37.50     43.75     18.75
one dice plus      33.33     33.33     33.33
one dice           50.00     25.00     25.00\
""",
    plotabledata = {
        "x": [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],  # Outcomes on x
        "y": [0, 1, 2, 3] * 3,  # Pools on y
        "z": [0] * 12,
        "dx": [1] * 12,
        "dy": [1] * 12,
        "dz": pytest.approx(
            [
                0.111111111111, 0.375, 0.33333333333, 0.5, # under 4
                0.555555555556, 0.4375, 0.33333333333, 0.25, # 5 or 6
                0.333333333333, 0.1875, 0.33333333333, 0.25, # over 6
            ],
        ),  # Grouped by outcomes then pools
        "color": [
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2), # two dice plus, under 4
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2), # two dice, under 4
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2), # one dice plus, under 4
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2), # one dice, under 4
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2), # two dice plus, 5 or 6
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2), # two dice, 5 or 6
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2), # one dice plus, 5 or 6
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2), # one dice, 5 or 6
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2), # two dice plus, over 6
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2), # two dice, over 6
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2), # one dice plus, over 6
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2), # one dice, over 6
        ],
    },
)
# fmt: on

PoolTests = {
    "namedpools": namedpools,
}

@pytest.mark.parametrize(
    ["pools", "outcomes", "chances"],
    [pytest.param(test.pools, test.outcomes, test.chances, id=testid) for testid, test in PoolTests.items()],
)
def test_chances(pools, outcomes, chances):
    pool = PoolComparison(pools, outcomes)
    assert pool.chances == pytest.approx(chances)

@pytest.mark.parametrize(
    ["pools", "outcomes", "table"],
    [pytest.param(test.pools, test.outcomes, test.table, id=testid) for testid, test in PoolTests.items()],
)
def test_table(pools, outcomes, table):
    pool = PoolComparison(pools, outcomes)
    assert str(pool) == table

@pytest.mark.parametrize(
    ["pools", "outcomes", "plotabledata"],
    [pytest.param(test.pools, test.outcomes, test.plotabledata, id=testid) for testid, test in PoolTests.items()],
)
def test_plotabledata(pools, outcomes, plotabledata):
    pool = PoolComparison(pools, outcomes)
    assert pool.plotable() == plotabledata