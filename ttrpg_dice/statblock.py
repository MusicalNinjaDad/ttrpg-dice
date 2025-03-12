"""Create statblocks easily."""

from dataclasses import dataclass

from .dice import Dice


class StatBlock:
    """A TTRPG StatBlock."""

def statblock(cls: type) -> StatBlock:
    """Create a StatBlock with the given fields."""

    def wrap(cls: type):
        stats = {statname for statname, roll in vars(cls).items() if isinstance(roll, Dice)}
        _interimclass: type = type(
            cls.__name__,
            (StatBlock,),
            {attr: 0 if attr in stats else val for attr, val in vars(cls).items()},
        )
        _interimclass.__annotations__ = {stat: int for stat in stats}
        return dataclass(_interimclass)

    return wrap(cls)
