import mpl_toolkits, matplotlib
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

unnamedpools = [2*d(4), d(6)+2, d(8)]
unnamedpools_dict = {2*d(4): 2*d(4), d(6)+2: d(6)+2, d(8): d(8)}

namedoutcomes = {
    "under 4": slice(None, 5),
    "5 or 6": slice(5,7),
    "over 6": slice(7,None),
}

chances = {
    ("2d4", "under 4"): 0.375,
    ("2d4", "5 or 6"): 0.4375,
    ("2d4", "over 6"): 0.1875,
    ("d6 + 2", "under 4"): 0.33333333333,
    ("d6 + 2", "5 or 6"): 0.33333333333,
    ("d6 + 2", "over 6"): 0.33333333333,
    ("d8", "under 4"): 0.5,
    ("d8", "5 or 6"): 0.25,
    ("d8", "over 6"): 0.25,
}

chances_bypool = {
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

chances_byoutcome = {
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

@pytest.mark.parametrize(
    ["inputpool", "storedpool"],
    [
        pytest.param(namedpools, namedpools, id="named pools"),
        pytest.param(unnamedpools, unnamedpools_dict, id="unnamend pools"),
    ],
)
def test_instatiation(inputpool, storedpool):
    comparison = PoolComparison(inputpool, namedoutcomes)
    assert comparison.pools == storedpool
    assert comparison.outcomes == namedoutcomes


def test_chances_no_extra_entries(named_pools_comparison):
    assert named_pools_comparison.chances.keys() == chances.keys()


@pytest.mark.parametrize(
    ["combo", "chance"],
    [pytest.param(combo, chance) for combo, chance in chances.items()],
)
def test_chances(named_pools_comparison, combo, chance):
    assert named_pools_comparison.chances[combo] == pytest.approx(chance)

def test_plot(named_pools_comparison: PoolComparison):
    fig, ax = named_pools_comparison.plot()
    assert isinstance(ax, mpl_toolkits.mplot3d.axes3d.Axes3D)
    assert isinstance(fig, matplotlib.figure.Figure)

# ==== Old API =======

@pytest.mark.parametrize(
    "pool",
    [pytest.param(pool) for pool in namedpools],
)
def test_named_pools(pool, named_pools_comparison: PoolComparison):
    assert named_pools_comparison.chances_bypool[pool] == pytest.approx(chances_bypool[pool])

@pytest.mark.parametrize(
    "die",
    [pytest.param(die, id=testid) for testid, die in namedpools.items()],
)
def test_unnamed_pools(die, unnamed_pools_comparison: PoolComparison):
    assert unnamed_pools_comparison.chances_bypool[die] == pytest.approx(chances_bypool[str(die)])

@pytest.mark.parametrize(
    "outcome",
    [pytest.param(outcome) for outcome in namedoutcomes],
)
def test_outcomes(outcome, named_pools_comparison: PoolComparison):
    assert named_pools_comparison.chances_byoutcome[outcome] == pytest.approx(chances_byoutcome[outcome])

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