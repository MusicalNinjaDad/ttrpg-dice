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

# TODO: Subclass StatBlock with specific values
# TODO: Immutable (frozen = True, test: hashable)
# TODO: Addition
# TODO: Max value assignable based on defined roll