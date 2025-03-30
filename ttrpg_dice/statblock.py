"""Create statblocks easily."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .dice import Dice

if TYPE_CHECKING:
    from contextlib import suppress

    with suppress(ImportError):
        from typing import ClassVar, Self


class StatBlock:
    """A TTRPG StatBlock."""

    _STATS: ClassVar[dict[str, Dice]]

    def __init__(self, *_args, **_kwargs) -> None:  # noqa: ANN002, ANN003
        """Do not directly instantiate a StatBlock, please use the @statblock decorator instead."""
        msg = "Cannot directly instantiate a StatBlock, please use the @statblock decorator instead."
        raise TypeError(msg)

    def _real_init_(self, /, **stats: dict[str, int | Dice]) -> None:
        """Initialise a Statblock with some, or all stats given."""
        for stat in self._STATS:
            val = stats.get(stat, vars(type(self)).get(stat))
            setattr(self, stat, val)

    def __add__(self, other: Self) -> Self:
        """Adds each stat, raises AttributeError if stat missing in `other`."""
        newstats = {
            stat: min(getattr(self, stat) + getattr(other, stat), len(self._STATS[stat])) for stat in self._STATS
        }
        return type(self)(**newstats)

    def __or__(self, other: Self) -> Self:
        """Merge stats, keeping the highest."""
        newstats = {stat: max(getattr(self, stat), getattr(other, stat)) for stat in self._STATS}
        return type(self)(**newstats)


def statblock(cls: type) -> StatBlock:
    """Create a StatBlock with the given fields."""
    stats = {statname: roll for statname, roll in vars(cls).items() if isinstance(roll, Dice)}
    _interimclass: type = type(
        cls.__name__,
        (cls, StatBlock),
        {attr: 0 if attr in stats else val for attr, val in vars(cls).items()},
    )
    _interimclass.__annotations__ = dict.fromkeys(stats, int | Dice)
    _interimclass._STATS = stats  # noqa: SLF001
    _interimclass.__init__ = StatBlock._real_init_
    return _interimclass
