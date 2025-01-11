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

    def __init__(self, faces: int) -> None:
        """Build a die."""
        self.probabilities = [None] + faces*[1/faces]
        """List of P(result) where result is index of list. P(0) = `None`"""
        
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

    # Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below
    # pytype: disable=invalid-annotation  # noqa: ERA001
    def __rmul__(self, other: SupportsInt) -> Self:
        """2 * Dice(4) returns a Dice with probabilities for 2d4."""
        other = self._int(other, "multiply", "by")
        rolls = [sum(r) for r in product(self.faces, repeat=other)]
        return self._from_possiblerolls(rolls)
    
    def __mul__(self, other: SupportsInt) -> Self:
        """Multiply result by constant."""
        other = self._int(other, "multiply", "by")
        rolls = [r * other for r in self.faces]
        return self._from_possiblerolls(rolls)

    def _int(self, other: SupportsInt, action: str, conjunction: str) -> int:
        try:
            other = int(other)
        except TypeError as e:
            msg=f"Cannot {action} '{type(other).__name__}' {conjunction} '{type(self).__name__}'"
            raise TypeError(msg) from e
        except ValueError as e:
            msg = f"Cannot {action} '{other}' {conjunction} '{type(self).__name__}'."
            msg += " (Hint: try using a string which only contains numbers)"
            raise TypeError(msg) from e
        return other

    def __add__(self, other: Self | SupportsInt) -> Self:
        """Adding two Dice to gives the combined roll."""
        try:
            rolls = [sum(r) for r in product(self.faces, other.faces)] # pytype: disable=attribute-error
        except AttributeError:
            other = self._int(other, "add", "and")
            rolls = [r + other for r in self.faces]
        return self._from_possiblerolls(rolls)

    @classmethod
    def _from_possiblerolls(cls, rolls: list[int]) -> Self:
        """Create a new die from a list of possible rolls."""
        possibilities = [None] + ([0] * max(rolls))
        for r in rolls:
            possibilities[r] += 1
        total_possibilities = sum(possibilities[1:])
        probabilities = [None] + [n / total_possibilities for n in possibilities[1:]]
        return cls.from_probabilities(probabilities)

    @classmethod
    def from_probabilities(cls, probabilities: list[float]) -> Self:
        """Create a new die with a given set of probabilities."""
        die = cls.__new__(cls)
        die.probabilities = probabilities
        return die
    # pytype: enable=invalid-annotation  # noqa: ERA001
    # END Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below