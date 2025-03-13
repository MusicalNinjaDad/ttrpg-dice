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

# TODO: Immutable (frozen = True, test: hashable)
# TODO: Union (highest from each stat)
# TODO: Max value assignable based on defined roll
# TODO: kw_only
# TODO: type-hinting instances (https://docs.python.org/3/library/typing.html#typing.get_type_hints)
# TODO: Handle `@statblock()` usage