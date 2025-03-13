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
    class Combat:
        WS = d(100)
        Dex = d(100)

    fighter = Combat(WS=41)

    assert fighter.WS == 41
    assert fighter.Dex == 0


# TODO: Immutable (frozen = True, test: hashable)
# TODO: Addition
# TODO: Max value assignable based on defined roll
# TODO: kw_only
# TODO: type-hinting instances