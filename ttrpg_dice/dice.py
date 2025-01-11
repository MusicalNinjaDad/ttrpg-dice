"""A Dice class."""

from collections.abc import Iterator
from itertools import product
from typing import Self


class Dice:
    """A Dice class."""

    def __init__(self, faces: int) -> None:
        """Build a die."""
        self.probabilities = [None] + faces*[1/faces]
        """List of P(result) where result is index of list. P(0) = `None`"""
        self.numfaces = faces
        self.faces = range(1,faces+1)

    def __iter__(self) -> Iterator:
        """Iterating over a Dice yields the probabilities starting with P(1)."""
        return iter(self.probabilities[1:])
    
    def __eq__(self, value: object) -> bool:
        """Dice are equal if they give the same probabilities."""
        try:
            return self.probabilities == value.probabilities # pytype: disable=attribute-error
        except AttributeError:
            return False

    def __rmul__(self, other: int) -> Self:
        """2 * Dice(4) returns a Dice with probabilities for 2d4."""
        rolls = [sum(r) for r in product(self.faces, repeat=other)]
        possibilities = [0] * (max(rolls)+1)
        for r in rolls:
            possibilities[r] += 1
        total_possibilities = sum(possibilities)
        probabilities = [n / total_possibilities for n in possibilities]
        probabilities[0] = None
        combo = Dice(1)
        combo.probabilities = probabilities
        return combo

    @classmethod
    def from_probabilities(cls, probabilities: list[float]) -> Self:
        """Create a new die with a given set of probabilities."""
        die = cls.__new__(cls)
        die.probabilities = probabilities
        die.numfaces = len(probabilities)-1
        return die