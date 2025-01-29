from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest  # noqa: F401, RUF100

from ttrpg_dice import d
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
    outcomes: dict[Any, slice]
    poolnames: list[str] | None = None
    poolsdict: dict[Any, d] | None = None
    outcomenames: list[str] | None = None
    chances: dict[tuple[Any, Any], float] | None = None
    table: str | None = None
    plotabledata: dict[str, list] | None = None
    plotformating: dict[str, Any] | None = None


# fmt: off
namedpools = PoolTestCase(
    pools={
        "two dice plus": (2*d(3)) + 2,
        "two dice": 2*d(4),
        "one dice plus": d(6)+2,
        "one dice": d(8),
    },
    poolnames=["two dice plus", "two dice", "one dice plus", "one dice"],
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
    outcomenames=["under 4", "5 or 6", "over 6"],
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
    plotformating={
        "xticks": [0.5, 1.5, 2.5], # Outcomes
        "yticks": [0.5, 1.5, 2.5, 3.5], # Pools
    },
)
# fmt: on

# fmt: off
unnamedpools = PoolTestCase(
    pools=[(2*d(3)) + 2, 2*d(4), d(6) + 2, d(8)],
    poolnames=["2d3 + 2", "2d4", "d6 + 2", "d8"],
    poolsdict={
        (2*d(3)) + 2: (2*d(3)) + 2,
        2*d(4): 2*d(4),
        d(6) + 2: d(6) + 2,
        d(8): d(8),
    },
    outcomes={
        "under 4": slice(None, 5),
        "5 or 6": slice(5, 7),
        "over 6": slice(7, None),
    },
    outcomenames=["under 4", "5 or 6", "over 6"],
    chances={
        ((2*d(3)) + 2, "under 4"): 0.111111111111,
        ((2*d(3)) + 2, "5 or 6"): 0.555555555556,
        ((2*d(3)) + 2, "over 6"): 0.333333333333,
        (2*d(4), "under 4"): 0.375,
        (2*d(4), "5 or 6"): 0.4375,
        (2*d(4), "over 6"): 0.1875,
        (d(6) + 2, "under 4"): 0.33333333333,
        (d(6) + 2, "5 or 6"): 0.33333333333,
        (d(6) + 2, "over 6"): 0.33333333333,
        (d(8), "under 4"): 0.5,
        (d(8), "5 or 6"): 0.25,
        (d(8), "over 6"): 0.25,
    },
    table="""\
pool       under 4    5 or 6    over 6
2d3 + 2      11.11     55.56     33.33
2d4          37.50     43.75     18.75
d6 + 2       33.33     33.33     33.33
d8           50.00     25.00     25.00\
""",
    plotabledata={
        "x": [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],  # Outcomes on x
        "y": [0, 1, 2, 3] * 3,  # Pools on y
        "z": [0] * 12,
        "dx": [1] * 12,
        "dy": [1] * 12,
        "dz": pytest.approx(
            [
                0.111111111111, 0.375, 0.33333333333, 0.5,  # under 4
                0.555555555556, 0.4375, 0.33333333333, 0.25,  # 5 or 6
                0.333333333333, 0.1875, 0.33333333333, 0.25,  # over 6
            ],
        ),  # Grouped by outcomes then pools
        "color": [
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # 2d3 + 2, under 4
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2),  # 2d4, under 4
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2),  # d6 + 2, under 4
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2),  # d8, under 4
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # 2d3 + 2, 5 or 6
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2),  # 2d4, 5 or 6
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2),  # d6 + 2, 5 or 6
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2),  # d8, 5 or 6
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # 2d3 + 2, over 6
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2),  # 2d4, over 6
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2),  # d6 + 2, over 6
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2),  # d8, over 6
        ],
    },
    plotformating={
        "xticks": [0.5, 1.5, 2.5],  # Outcomes
        "yticks": [0.5, 1.5, 2.5, 3.5],  # Pools
    },
)
# fmt: on

# fmt: off
manypools = PoolTestCase(
    pools=[d(4), d(6), d(8), d(10), d(12), d(20), d(100)],
    outcomes={
        "odds": slice(1, None, 2),
        "evens": slice(2, None, 2),
    },
    poolnames=["d4", "d6", "d8", "d10", "d12", "d20", "d100"],
    poolsdict={
        "d4": d(4),
        "d6": d(6),
        "d8": d(8),
        "d10": d(10),
        "d12": d(12),
        "d20": d(20),
        "d100": d(100),
    },
    outcomenames=["odds", "evens"],
    chances={
        (d(4), "odds"): 0.5,
        (d(4), "evens"): 0.5,
        (d(6), "odds"): 0.5,
        (d(6), "evens"): 0.5,
        (d(8), "odds"): 0.5,
        (d(8), "evens"): 0.5,
        (d(10), "odds"): 0.5,
        (d(10), "evens"): 0.5,
        (d(12), "odds"): 0.5,
        (d(12), "evens"): 0.5,
        (d(20), "odds"): 0.5,
        (d(20), "evens"): 0.5,
        (d(100), "odds"): 0.5,
        (d(100), "evens"): 0.5,
    },
    table="""\
pool      odds    evens
d4       50.00    50.00
d6       50.00    50.00
d8       50.00    50.00
d10      50.00    50.00
d12      50.00    50.00
d20      50.00    50.00
d100     50.00    50.00\
""",
    plotabledata={
        "x": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],  # Outcomes on x
        "y": [0, 1, 2, 3, 4, 5, 6] * 2,  # Pools on y
        "z": [0] * 14,
        "dx": [1] * 14,
        "dy": [1] * 14,
        "dz": pytest.approx([0.5] * 14),  # Grouped by outcomes then pools
        "color": [
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # d4, odds
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2),  # d6, odds
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2),  # d8, odds
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2),  # d10, odds
            ("m", 0), ("m", 1), ("m", 0), ("m", 0), ("m", 0.2), ("m", 0.2),  # d12, odds
            ("y", 0), ("y", 1), ("y", 0), ("y", 0), ("y", 0.2), ("y", 0.2),  # d20, odds
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # 100, odds
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # d4, evens
            ("g", 0), ("g", 1), ("g", 0), ("g", 0), ("g", 0.2), ("g", 0.2),  # d6, evens
            ("r", 0), ("r", 1), ("r", 0), ("r", 0), ("r", 0.2), ("r", 0.2),  # d8, evens
            ("c", 0), ("c", 1), ("c", 0), ("c", 0), ("c", 0.2), ("c", 0.2),  # d10, evens
            ("m", 0), ("m", 1), ("m", 0), ("m", 0), ("m", 0.2), ("m", 0.2),  # d12, evens
            ("y", 0), ("y", 1), ("y", 0), ("y", 0), ("y", 0.2), ("y", 0.2),  # d20, evens
            ("b", 0), ("b", 1), ("b", 0), ("b", 0), ("b", 0.2), ("b", 0.2),  # 100, evens
        ],
    },
    plotformating={
        "xticks": [0.5, 1.5],  # Outcomes
        "yticks": [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5],  # Pools
    },
)
# fmt: on


PoolTests = {
    "namedpools": namedpools,
    "unnamedpools": unnamedpools,
    "more pools than colours": manypools,
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


@pytest.mark.parametrize(
    ["pools", "outcomes", "poolnames", "outcomenames", "xticks", "yticks"],
    [
        pytest.param(
            test.pools,
            test.outcomes,
            test.poolnames,
            test.outcomenames,
            test.plotformating["xticks"],
            test.plotformating["yticks"],
            id=testid,
        )
        for testid, test in PoolTests.items()
    ],
)
def test_plot(pools, outcomes, poolnames, outcomenames, xticks, yticks):  # noqa: PLR0913
    pool = PoolComparison(pools, outcomes)
    fig, ax = pool.plot()
    assert [label.get_text() for label in ax.get_xmajorticklabels()] == outcomenames
    assert list(ax.get_xticks()) == xticks
    assert [label.get_text() for label in ax.get_ymajorticklabels()] == poolnames
    assert list(ax.get_yticks()) == yticks
