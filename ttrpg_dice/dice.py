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
            return self._probabilities # pytype: disable=attribute-error
        except AttributeError:
            components = self._unpackcontents()
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
    def weighted(self) -> bool:
        """Is this Dice weighted, or are all results equally likely?"""
        return min(self.probabilities[1:]) != max(self.probabilities[1:])

    def __iter__(self) -> Iterator:
        """Iterating over a Dice yields the probabilities starting with P(1)."""
        return iter(self.probabilities[1:])
    
    def __getitem__(self, index: int | slice) -> float | list[float] | None:
        """Get the probability of a specific result."""
        try:
            if index.start is None:
                index = slice(1,index.stop,index.step)
            if (index.start < 1) or (index.stop is not None and index.stop < 1):
                raise DiceIndexError(self, index)
        except AttributeError:
            pass
        if index == 0: raise DiceIndexError(self, index)
        try: 
            return self.probabilities[index]
        except TypeError as e:
            msg = f"Cannot index '{type(self).__name__}' with '{type(index).__name__}'"
            raise TypeError(msg) from e
        except IndexError as e:
            raise DiceIndexError(self, index) from e

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
        return self.from_contents(defaultdict(int, {f:n*other for f, n in self.contents.items()}))

    def __add__(self, other: Self | SupportsInt) -> Self:
        """Adding two Dice to gives the combined roll."""
        try:
            othercontents = other.contents # pytype: disable=attribute-error
        except AttributeError:
            othercontents = defaultdict(int, {1: self._int(other, "add", "and")})
        contents = defaultdict(
                int,
                {
                    faces: self.contents[faces] + othercontents[faces]
                    for faces in self.contents.keys() | othercontents.keys()
                },
            )
        return self.from_contents(contents)

    @classmethod
    def from_contents(cls, contents: defaultdict) -> Self:
        """Create a new die from a dict of contents."""
        die = cls.__new__(cls)
        die.contents = contents
        return die
    # pytype: enable=invalid-annotation
    # END Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below

    def _unpackcontents(self) -> Generator[list, None, None]:
        """What's in that contents dict?"""
        for faces, numdice in self.contents.items():
            yield from repeat(list(range(1,faces+1)),numdice)

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

class DiceIndexError(IndexError):
    """
    Exception raised for errors in the indexing of a Dice object.

    Attributes:
        dice (Dice): The Dice object where the error occurred.
        index (int): The index that caused the error.
    """

    def __init__(self, dice: Dice, index: int) -> None:
        """
        Initialize the DiceIndexError with the given Dice object and index.

        Args:
            dice (Dice): The Dice object where the error occurred.
            index (int): The index that caused the error.
        """
        self.dice = dice
        self.index = index
        super().__init__(self._error_message())

    def _error_message(self) -> str:
        """
        Generate the error message for the exception.

        Returns:
            str: The error message indicating the index is out of bounds.
        """
        return f"Index out of bounds, this Dice has sides numbered 1 to {len(self.dice.probabilities) - 1}"