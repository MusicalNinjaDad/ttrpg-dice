import pytest  # noqa: F401, RUF100

from ttrpg_dice import Dice as d  # noqa: N813
from ttrpg_dice import evaluatepool


def test_pool():
    chances = {
            "nicehumanoid": 0.06944444444444445,
            "neutral": 0.5486111111111112,
            "nastyhumanoid": 0.2777777777777778,
            "nastyanimal": 0.06944444444444445,
    }
    die = 2 * d(12)
    encounters = {
            "nicehumanoid": slice(None, 6),
            "neutral": slice(6, 15),
            "nastyhumanoid": slice(15, 20),
            "nastyanimal": slice(21, None),
    }
    assert evaluatepool(die, encounters) == chances