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

namedpools = {
    "2d4": 2*d(4),
    "d6 + 2": d(6)+2,
    "d8": d(8),
}

namedoutcomes = {
    "under 4": slice(None, 5),
    "5 or 6": slice(5,7),
    "over 6": slice(7,None),
}

chances = {
    "2d4": {
        "under 4": 0.375,
        "5 or 6": 0.4375,
        "over 6": 0.1875,
    },
    "d6 + 2": {
        "under 4": 0.33333333333,
        "5 or 6": 0.33333333333,
        "over 6": 0.33333333333,
    },
    "d8": {
        "under 4": 0.5,
        "5 or 6": 0.25,
        "over 6": 0.25,
    },
}

chances_transposed = {
    "under 4": {
        "2d4": 0.375,
        "d6 + 2": 0.33333333333,
        "d8": 0.5,
    },
    "5 or 6": {
        "2d4": 0.4375,
        "d6 + 2": 0.33333333333,
        "d8": 0.25,
    },
    "over 6": {
        "2d4": 0.1875,
        "d6 + 2": 0.33333333333,
        "d8": 0.25,
    },
}

@pytest.fixture
def named_pools_comparison() -> PoolComparison:
    return PoolComparison(namedpools, namedoutcomes)

@pytest.fixture
def unnamed_pools_comparison() -> PoolComparison:
    return PoolComparison(namedpools.values(), namedoutcomes)

# ==== New API =======




# ==== Old API =======

@pytest.mark.parametrize(
    "pool",
    [pytest.param(pool) for pool in namedpools],
)
def test_named_pools(pool, named_pools_comparison: PoolComparison):
    assert named_pools_comparison.chances_bypool[pool] == pytest.approx(chances[pool])

@pytest.mark.parametrize(
    "die",
    [pytest.param(die, id=testid) for testid, die in namedpools.items()],
)
def test_unnamed_pools(die, unnamed_pools_comparison: PoolComparison):
    assert unnamed_pools_comparison.chances_bypool[die] == pytest.approx(chances[str(die)])

@pytest.mark.parametrize(
    "outcome",
    [pytest.param(outcome) for outcome in namedoutcomes],
)
def test_outcomes(outcome, named_pools_comparison: PoolComparison):
    assert named_pools_comparison.chances_byoutcome[outcome] == pytest.approx(chances_transposed[outcome])

formatted = """\
pool      under 4    5 or 6    over 6
2d4         37.50     43.75     18.75
d6 + 2      33.33     33.33     33.33
d8          50.00     25.00     25.00\
"""

def test_format_named(named_pools_comparison: PoolComparison):
    assert str(named_pools_comparison) == formatted

formatted = """\
pool      under 4    5 or 6    over 6
2d4         37.50     43.75     18.75
d6 + 2      33.33     33.33     33.33
d8          50.00     25.00     25.00\
"""

def test_format_unnamed(unnamed_pools_comparison: PoolComparison):
    assert str(unnamed_pools_comparison) == formatted

# TO-DO
#
# Revamp the test cases to give pools names which are not same as Dice