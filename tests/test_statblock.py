from ttrpg_dice import d, statblock


def test_empty():
    @statblock
    class Combat:
        WS = d(100)

    empty = Combat()
    assert empty.WS == 0
