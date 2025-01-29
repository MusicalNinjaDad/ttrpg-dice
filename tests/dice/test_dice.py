import re

import pytest  # noqa: F401, RUF100

from ttrpg_dice import d


def test_eq():
    d4 = d(4)
    assert d4 is not d(4)
    assert d4 == d(4)


def test_inequality():
    d4 = d(4)
    d6 = d(6)
    assert d4 != d6
    assert d4 != [None, 0.25, 0.25, 0.25, 0.25]


def test_no_sideeffects_add():
    d2 = d(2)
    adv = d2 + 1
    assert adv == d(2) + 1
    assert d2 == d(2)


def test_add_float():
    assert d(4) + 2.0 == d(4) + 2


def test_add_string():
    assert d(4) + "2" == d(4) + 2


def test_add_two():
    msg = re.escape("Cannot add 'two' and 'Dice'. (Hint: try using a string which only contains numbers)")
    with pytest.raises(TypeError, match=msg):
        d(4) + "two"


def test_add_None():
    with pytest.raises(TypeError, match="Cannot add 'NoneType' and 'Dice'"):
        d(4) + None


def test_no_sideeffects_rmul():
    d4 = d(4)
    roll = 2 * d4
    assert roll == 2 * d(4)
    assert d4 == d(4)


def test_floatxDice():
    assert 2.0000001 * d(4) == 2 * d(4)


def test_stringxDice():
    assert "2" * d(4) == 2 * d(4)


def test_twoxDice():
    msg = re.escape("Cannot multiply 'two' by 'Dice'. (Hint: try using a string which only contains numbers)")
    with pytest.raises(TypeError, match=msg):
        "two" * d(4)


def test_NonexDice():
    with pytest.raises(TypeError, match="Cannot multiply 'NoneType' by 'Dice'"):
        None * d(4)


def test_cannot_change_probabilities():
    d4 = d(4)
    msg = re.escape("You cannot change a Dice's probabilities, create a new Dice instead.")
    with pytest.raises(AttributeError, match=msg):
        d4._probabilities = [1, 2]  # noqa: SLF001


def test_individualrolls():
    die = d.from_contents({2: 1, 4: 2, 1: 3})
    assert list(die._individual_dice_rolls()) == [[1, 2], [1, 2, 3, 4], [1, 2, 3, 4], [1], [1], [1]]  # noqa: SLF001


def test_immutable():
    d4 = d(4)
    assert d4.contents[4] == 1
    with pytest.raises(TypeError, match="Dice contents cannot be changed"):
        d4.contents[4] = 2
    assert d4.contents[4] == 1


def test_no_unwanted_mutations():
    d4 = d(4)
    assert len(d4.contents) == 1
    cached_hash = hash(d4)
    assert d4.contents[5] == 0 # does not contain a d5
    assert len(d4.contents) == 1 # checking for d5 did not add an entry 5 : 0 to the contents, as a defaultdict would
    assert hash(d4) == cached_hash # or change the hash


def test_remove_zeros():
    dice = d.from_contents({1: 0, 4: 1, 3: 0, 6: 2, 8: 0})
    assert dice.contents == {4: 1, 6: 2}
