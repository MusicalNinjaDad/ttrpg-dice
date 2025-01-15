import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813
from ttrpg_dice import evaluatepool

# Anydice calculation:
# function: range on DIE:n between LOW:n and HIGH:n {
# if DIE >= LOW & DIE <= HIGH { result: 1 }
# result: 0
# }

# POOL: 2d4

# output [range on POOL between 1 and 4]
# output [range on POOL between 5 and 6]
# output [range on POOL between 7 and 8]

pools = {
    "2d4": 2*d(4),
    "d6 + 2": d(6)+2,
    "d8": d(8),
}

outcomes = {
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

def test_pools():
    results = evaluatepool(pools, outcomes)
    for pool, result in results.items():
        assert result == pytest.approx(chances[pool])