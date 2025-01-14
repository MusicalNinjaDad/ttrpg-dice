"""A Dice class."""
from __future__ import annotations

from collections import defaultdict, deque
from itertools import product, repeat
from typing import TYPE_CHECKING, SupportsInt

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self  # required for Python3.10 and below


class Dice:
    """A Dice class."""

    def __init__(self, faces: int) -> None:
        """Build a die."""
        self.contents = defaultdict(int, {faces:1})
        
    @property
    def probabilities(self) -> list[float | None]:
        """List of P(result) where result is index of list. P(0) = `None`."""
        try:
            return self._probabilities
        except AttributeError:
            components = self._unpackcontents(self.contents)
            rolls = [sum(r) for r in product(*components)]
            possibilities = [None] + ([0] * max(rolls))
            for r in rolls:
                possibilities[r] += 1
            total_possibilities = sum(possibilities[1:])
            self._probabilities = [None] + [n / total_possibilities for n in possibilities[1:]]
            return self._probabilities

    @probabilities.setter
    def probabilities(self, _: None) -> None:
        msg = "You cannot change a Dice's probabilities, create a new Dice instead."
        raise AttributeError(msg)

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
        sortedcontents = deque(sorted(self.contents.items()))
        if sortedcontents[0][0] == 1: sortedcontents.rotate(-1)
        return " + ".join(f"{n if n > 1 or x == 1 else ''}d{x if x > 1 else ''}" for x, n in sortedcontents).rstrip("d")

    # Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below
    # pytype: disable=invalid-annotation
    def __rmul__(self, other: SupportsInt) -> Self:
        """2 * Dice(4) returns a Dice with probabilities for 2d4."""
        other = self._int(other, "multiply", "by")
        return self.from_contents(defaultdict(int, {self.numfaces: other}))

    def __add__(self, other: Self | SupportsInt) -> Self:
        """Adding two Dice to gives the combined roll."""
        try:
            # pytype: disable=attribute-error
            contents = defaultdict(
                int,
                {
                    faces: self.contents[faces] + other.contents[faces]
                    for faces in self.contents.keys() | other.contents.keys()
                },
            )
            # pytype: enable=attribute-error
        except AttributeError:
            other = self._int(other, "add", "and")
            contents = self.contents
            contents[1] += other
        return self.from_contents(contents)

    @classmethod
    def from_contents(cls, contents: defaultdict) -> Self:
        """Create a new die from a dict of contents."""
        die = cls.__new__(cls)
        die.contents = contents
        return die
    # pytype: enable=invalid-annotation
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
    
    @classmethod
    def _unpackcontents(cls, contents: dict) -> Generator[list, None, None]:
        """What's in that contents dict?"""
        for faces, numdice in contents.items():
            yield from repeat(list(range(1,faces+1)),numdice)
