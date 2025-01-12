"""A Dice class."""
from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING, SupportsInt

if TYPE_CHECKING:
    from collections.abc import Iterator

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self  # required for Python3.10 and below


class Dice:
    """A Dice class."""

    def __init__(self, faces: int, description: str = "") -> None:
        """Build a die."""
        self.probabilities = [None] + faces*[1/faces]
        if description:
            self.description = description
        else:
            self.description = f"d{self.numfaces}"

    @property
    def probabilities(self) -> list[float | None]:
        """List of P(result) where result is index of list. P(0) = `None`."""
        return self._probabilities

    @probabilities.setter
    def probabilities(self, value: list[float | None]) -> None:
        if hasattr(self,"_probabilities"):
            msg = "You cannot change a Dice's probabilities, create a new Dice instead."
            raise AttributeError(msg)
        if value[0] is not None:
            msg = "First probability, P(0), must be `None`"
            raise ValueError(msg)
        if value.count(None) > 1:
            msg = "Only the first probability, P(0), may be `None`"
            raise ValueError(msg)
        if sum(value[1:]) != 1:
            msg = f"Dice probabilities must sum to 1 (not {sum(value[1:])})"
            raise ValueError(msg)
        self._probabilities = value

    @property
    def numfaces(self) -> int:
        """How faces this Dice has."""
        return len(self.probabilities)-1

    @property
    def faces(self) -> range:
        """Range of available faces on this Dice."""
        return range(1,self.numfaces+1)
    
    @property
    def weighted(self) -> bool:
        """Is this Dice weighted, or are all results equally likely?"""
        return min(self.probabilities[1:]) != max(self.probabilities[1:])

    def __iter__(self) -> Iterator:
        """Iterating over a Dice yields the probabilities starting with P(1)."""
        return iter(self.probabilities[1:])
    
    def __eq__(self, value: object) -> bool:
        """Dice are equal if they give the same probabilities."""
        try:
            return self.probabilities == value.probabilities # pytype: disable=attribute-error
        except AttributeError:
            return False
        
    def __str__(self) -> str:
        """The type of Dice in NdX notation."""
        return self.description

    # Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below
    # pytype: disable=invalid-annotation  # noqa: ERA001
    def __rmul__(self, other: SupportsInt) -> Self:
        """2 * Dice(4) returns a Dice with probabilities for 2d4."""
        other = self._int(other, "multiply", "by")
        rolls = [sum(r) for r in product(self.faces, repeat=other)]
        return self._from_possiblerolls(rolls, description=f"{other}{self}")
    
    def __mul__(self, other: SupportsInt) -> Self:
        """Multiply result by constant."""
        other = self._int(other, "multiply", "by")
        rolls = [r * other for r in self.faces]
        return self._from_possiblerolls(rolls, description=f"{self}*{other}")

    def __add__(self, other: Self | SupportsInt) -> Self:
        """Adding two Dice to gives the combined roll."""
        try:
             # pytype: disable=attribute-error  # noqa: ERA001
            rolls = [sum(r) for r in product(self.faces, other.faces)]
            descr = f"{self.description} + {other.description}"
            # pytype: enable=attribute-error  # noqa: ERA001
        except AttributeError:
            other = self._int(other, "add", "and")
            rolls = [r + other for r in self.faces]
            descr = f"{self.description} + {other}"
        return self._from_possiblerolls(rolls, descr)

    @classmethod
    def _from_possiblerolls(cls, rolls: list[int], description: str) -> Self:
        """Create a new die from a list of possible rolls."""
        possibilities = [None] + ([0] * max(rolls))
        for r in rolls:
            possibilities[r] += 1
        total_possibilities = sum(possibilities[1:])
        probabilities = [None] + [n / total_possibilities for n in possibilities[1:]]
        return cls.from_probabilities(probabilities, description)

    @classmethod
    def from_probabilities(cls, probabilities: list[float], description: str) -> Self:
        """Create a new die with a given set of probabilities."""
        die = cls.__new__(cls)
        die.probabilities = probabilities
        die.description = description
        return die
    # pytype: enable=invalid-annotation  # noqa: ERA001
    # END Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below

    @classmethod
    def _int(cls, other: SupportsInt, action: str, conjunction: str) -> int:
        """Attempts to convert `other` to an int for use in arithmetic magic methods."""
        try:
            other = int(other)
        except TypeError as e:
            msg=f"Cannot {action} '{type(other).__name__}' {conjunction} '{cls.__name__}'"
            raise TypeError(msg) from e
        except ValueError as e:
            msg = f"Cannot {action} '{other}' {conjunction} '{cls.__name__}'."
            msg += " (Hint: try using a string which only contains numbers)"
            raise TypeError(msg) from e
        return other