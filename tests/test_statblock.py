import dataclasses
import re

import pytest

from ttrpg_dice import StatBlock, d, statblock


def test_empty():
    @statblock
    class Combat:
        WS = d(100)

    empty = Combat()
    assert empty.WS == 0


def test_isinstance_StatBlock():
    @statblock
    class Combat:
        WS = d(100)

    empty = Combat()
    assert isinstance(empty, StatBlock)


def test_instatiation():
    @statblock
    class Mixed:
        WS = d(100)
        Dex = d(100)

    fighter = Mixed(WS=41)

    assert fighter.WS == 41
    assert fighter.Dex == 0
    assert isinstance(fighter, StatBlock)
    assert type(fighter) is Mixed


def test_addition():
    @statblock
    class Combat:
        WS = d(100)

    fighter = Combat(WS=41)
    skilled = Combat(WS=10)

    knight = fighter + skilled

    assert knight.WS == 51
    assert isinstance(knight, Combat)


def test_instance_vars():
    @statblock
    class Combat:
        WS = d(100)

    fighter = Combat(WS=41)
    assert vars(fighter) == {"WS": 41}


def test__STATS():
    @statblock
    class Combat:
        WS = d(100)

    fighter = Combat(WS=41)

    assert fighter._STATS == {"WS": d(100)}  # noqa: SLF001


def test_maxed_out():
    @statblock
    class Combat:
        WS = d(100)

    fighter = Combat(WS=41)
    superhuman = Combat(WS=60)

    hero = fighter + superhuman

    assert hero.WS == 100


def test_union():
    @statblock
    class FullCombat:
        WS = d(100)
        BS = d(100)

    squire = FullCombat(WS=10, BS=10)
    thief = FullCombat(WS=20)

    runaway = squire | thief

    assert runaway.WS == 20
    assert runaway.BS == 10


def test_no_direct_instantiation():
    msg = re.escape("Cannot directly instantiate a StatBlock, please use the @statblock decorator instead.")
    with pytest.raises(TypeError, match=msg):
        _ = StatBlock()


def test_no_direct_instantiation_with_args():
    msg = re.escape("Cannot directly instantiate a StatBlock, please use the @statblock decorator instead.")
    with pytest.raises(TypeError, match=msg):
        _ = StatBlock(WS=7)


def test_subclass_has__STATS():
    @statblock
    class Combat:
        WS = d(100)

    class Human(Combat):
        WS = 33

    albert = Human()
    assert albert._STATS == {"WS": d(100)}  # noqa: SLF001


def test_subclass_stat():
    @statblock
    class Combat:
        WS = d(100)

    @statblock
    class Human(Combat):
        WS = 33

    albert = Human()
    assert albert.WS == 33


def test_subclass_partial():
    @statblock
    class FullCombat:
        WS = d(100)
        BS = d(100)

    @statblock
    class Human(FullCombat):
        WS = 33

    albert = Human()
    assert vars(albert) == {"WS": 33, "BS": 0}


def test_kw_only():
    @statblock
    class FullCombat:
        WS = d(100)
        BS = d(100)

    with pytest.raises(TypeError):
        _ = FullCombat(45)

def test_immutable():
    @statblock
    class Combat:
        WS = d(100)

    fighter = Combat(WS=41)

    with pytest.raises(dataclasses.FrozenInstanceError):
        fighter.WS = 51

# TODO: type-hinting instances (https://docs.python.org/3/library/typing.html#typing.get_type_hints)
# TODO: Handle `@statblock()` usage
# TODO: Maths where blocks have different stats
