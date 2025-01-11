"""A Dice class."""

from collections.abc import Iterator
from itertools import product

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self  # type: ignore[reportMissingModuleSource]


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

    def __rmul__(self, other: int) -> Self: # pytype: disable=invalid-annotation
        """2 * Dice(4) returns a Dice with probabilities for 2d4."""
        rolls = [sum(r) for r in product(self.faces, repeat=other)]
        possibilities = [None] + ([0] * max(rolls))
        for r in rolls:
            possibilities[r] += 1
        total_possibilities = sum(possibilities[1:])
        probabilities = [None] + [n / total_possibilities for n in possibilities[1:]]
        return self.from_probabilities(probabilities)

    @classmethod
    def from_probabilities(cls, probabilities: list[float]) -> Self: # pytype: disable=invalid-annotation
        """Create a new die with a given set of probabilities."""
        die = cls.__new__(cls)
        die.probabilities = probabilities
        return die