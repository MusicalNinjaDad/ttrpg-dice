"""Create statblocks easily."""

from dataclasses import dataclass
from typing import ClassVar, Self

from .dice import Dice


class StatBlock:
    """A TTRPG StatBlock."""

    _STATS: ClassVar[dict[str,Dice]]

    def __add__(self, other: Self) -> Self:
        """Adds each stat, raises AttributeError if stat missing in `other`."""
        newstats = {stat: min(getattr(self,stat) + getattr(other,stat), len(self._STATS[stat]))
        for stat in self._STATS}
        return type(self)(**newstats)

    def __or__(self, other: Self) -> Self:
        """Merge stats, keeping the highest."""
        newstats = {stat: max(getattr(self,stat), getattr(other,stat))
        for stat in self._STATS}
        return type(self)(**newstats)
            
def statblock(cls: type) -> StatBlock:
    """Create a StatBlock with the given fields."""

    def wrap(cls: type):
        stats = {statname: roll for statname, roll in vars(cls).items() if isinstance(roll, Dice)}
        _interimclass: type = type(
            cls.__name__,
            (cls, StatBlock),
            {attr: 0 if attr in stats else val for attr, val in vars(cls).items()},
        )
        _interimclass.__annotations__ = {stat: int for stat in stats}
        _interimclass._STATS = stats  # noqa: SLF001
        return dataclass(_interimclass)

    return wrap(cls)
