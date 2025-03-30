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

    class _Contents(defaultdict):
        """Dice Contents are immutable after creation and return `0` if queried for a missing entry."""

        def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
            tempdict = dict(*args, **kwargs)
            super().__init__(int, {faces: numdice for faces, numdice in tempdict.items() if numdice != 0})
            self._validate()

        def _validate(self) -> None:
            """
            `Dice._probabilities()` is called lazily and will be very hard to debug if contents are not valid.

            - `range(1,faces)` requires positive `int`
            - `repeat(...,numdice)` requires postive `int`
            """
            int_faces = {faces: isinstance(faces, int) for faces in self.keys()}
            if not all(int_faces.values()):
                invalid = ", ".join(sorted(type(faces).__name__ for faces, isint in int_faces.items() if not isint))
                msg = f"Number of faces must be a positive integer, not {invalid}"
                raise TypeError(msg)

            positive_faces = {faces: faces > 0 for faces in self.keys()}
            if not all(positive_faces.values()):
                invalid = ", ".join(
                    str(faces) for faces, ispositive in sorted(positive_faces.items()) if not ispositive
                )
                msg = f"Number of faces must be a positive integer, not {invalid}"
                raise ValueError(msg)

            int_numdice = {faces: isinstance(numdice, int) for faces, numdice in self.items()}
            if not all(int_numdice.values()):
                invalid = ", ".join(
                    type(self[faces]).__name__ for faces, isint in sorted(int_numdice.items()) if not isint
                )
                msg = f"Number of Dice must be a positive integer, not {invalid}"
                raise TypeError(msg)

            positive_numdice = {faces: numdice > 0 for faces, numdice in self.items()}
            if not all(positive_numdice.values()):
                invalid = ", ".join(
                    str(self[faces]) for faces, ispositive in sorted(positive_numdice.items()) if not ispositive
                )
                msg = f"Number of Dice must be a positive integer, not {invalid}"
                raise ValueError(msg)

        def __setitem__(self, key: int, value: int):  # noqa: ANN204
            msg = "Dice contents cannot be changed"
            raise TypeError(msg)

        def __missing__(self, key):  # noqa: ANN001, ANN204
            """Does not set new entry if Contents are frozen."""
            return self.default_factory()

        def __hash__(self) -> int:
            """Hash contents as tuple of sorted (key, value) tuples."""
            return hash(tuple(sorted(self.items())))

    def __init__(self, faces: int) -> None:
        """Build a die with `faces` sides."""
        self.contents = self._Contents({faces: 1})

    @property
    def _probabilities(self) -> list[float | None]:
        """
        Use Dice[index] to get the probability(-ies) of a given (set of) roll(s) NOT _probabilities.

        If for some reason you MUST access the underlying probabilities list use this property and not
        Dice._probabilitycache which is created lazily on the first call to this method.

        Returns a list of P(result) with _probabilities[0] = `None`.
        """
        try:
            return self._probabilitycache  # pytype: disable=attribute-error
        except AttributeError:
            all_possible_rolls = [sum(r) for r in product(*self._individual_dice_rolls())]
            ways_to_roll = {roll: all_possible_rolls.count(roll) for roll in range(1, max(all_possible_rolls) + 1)}
            number_possible_rolls = len(all_possible_rolls)
            self._probabilitycache = [None] + [n / number_possible_rolls for _, n in sorted(ways_to_roll.items())]
            return self._probabilitycache

    @_probabilities.setter
    def _probabilities(self, _: None) -> None:
        msg = "You cannot change a Dice's probabilities, create a new Dice instead."
        raise AttributeError(msg)

    @property
    def weighted(self) -> bool:
        """Is this Dice weighted, or are all results equally likely?"""
        return min(self) != max(self)

    def __iter__(self) -> Iterator:
        """Iterating over a Dice yields the probabilities starting with P(1)."""
        yield from self._probabilities[1:]

    def __getitem__(self, index: int | slice) -> float | list[float] | None:
        """
        Get the probability of a specific result, or a list of probabilities in the case of a slice.

        This handles the fact that dice faces are numbered from 1, not 0. Slicing with a step > 1 will
        return the probabilities of results beginning with the given step, not beginning with 1.

        Example:
            ```
            >>> from ttrpg_dice import d
            >>> dice = 2 * d(2)
            >>> list(dice)
            [0.0, 0.25, 0.5, 0.25]

            >>> dice[:]
            [0.0, 0.25, 0.5, 0.25]

            >>> dice[1]
            0.0

            >>> dice[::2] # evens
            [0.25, 0.25]

            >>> dice[1::2] # odds
            [0.0, 0.5]
            ```
        """
        if index == 0 or index == -(len(self) + 1):
            raise DiceIndexError(self)

        try:
            # pytype: disable=attribute-error
            if index.step is None or index.step > 0:  # Positive step
                if index.start is None:
                    index = slice(1 if index.step is None else index.step, index.stop, index.step)
                elif index.start == 0:  # To avoid possible confusion by slicing [0:]
                    raise DiceIndexError(self)
            else:  # Negative Step  # noqa: PLR5501
                if index.stop is None:
                    index = slice(index.start, 0, index.step)
            # pytype: enable=attribute-error
        except AttributeError:
            pass

        try:
            return self._probabilities[index]
        except TypeError as e:
            msg = f"Cannot index '{type(self).__name__}' with '{type(index).__name__}'."
            raise TypeError(msg) from e
        except IndexError as e:
            raise DiceIndexError(self) from e

    def __eq__(self, value: object) -> bool:
        """Dice are equal if they give the same probabilities, even with different contents."""
        try:
            return self._probabilities == value._probabilities  # pytype: disable=attribute-error
        except AttributeError:
            return False

    def __hash__(self) -> int:
        """Use contents for hashing - but NOT equality."""
        return hash(self.contents)

    def __len__(self) -> int:
        """Number of faces."""
        return len(self._probabilities) - 1

    def __str__(self) -> str:
        """The type of Dice in NdX notation."""
        sortedcontents = deque(sorted(self.contents.items()))

        # Place any constant at the end ("d4 + 2" not "2 + d4")
        if sortedcontents[0][0] == 1:
            sortedcontents.rotate(-1)

        def _ndx(n: int, x: int) -> str:
            if x == 1:
                return str(n)
            return f"{n if n > 1 else ''}d{x}"

        return " + ".join(_ndx(n, x) for x, n in sortedcontents)

    def __repr__(self) -> str:
        """Classname: ndX (contents)."""
        contents = ", ".join([f"{d}: {n}" for d, n in self.contents.items()])
        return f"{type(self).__name__}: {self} ({{{contents}}})"

    # =================
    # Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below
    # pytype: disable=invalid-annotation

    def __rmul__(self, other: SupportsInt) -> Self:
        """2 * Dice(4) returns a Dice with probabilities for 2d4."""
        other = self._int(other, "multiply", "by")
        return self.from_contents({f: n * other for f, n in self.contents.items()})

    def __add__(self, other: Self | SupportsInt) -> Self:
        """Adding two Dice to gives the combined roll."""
        try:
            othercontents = other.contents  # pytype: disable=attribute-error
        except AttributeError:
            othercontents = defaultdict(int, {1: self._int(other, "add", "and")})

        contents = {
            face: self.contents[face] + othercontents[face] for face in set(self.contents.keys() | othercontents.keys())
        }

        return self.from_contents(contents)

    @classmethod
    def from_contents(cls, contents: dict) -> Self:
        """Create a new die from a dict of contents."""
        die = cls.__new__(cls)
        die.contents = cls._Contents(contents)
        return die
    
    @classmethod
    def from_str(cls, description: str) -> Self:
        """Create a new die from ndX notation."""
        dice = description.split("+")
        contents = {
            int(x) if x else 1: int(n) if n else 1
            for die in dice
            for n, d, x in [die.strip().partition("d")]
        }
        return cls.from_contents(contents)

    # pytype: enable=invalid-annotation
    # END Block of stuff that returns Self ... pytype doesn't like this while we have Python3.10 and below
    # =================

    def _individual_dice_rolls(self) -> Generator[list, None, None]:
        """
        Yields a series of lists, each containing the valid faces of the individual dice contained within this `Dice`.

        Examples:
            For a simple d4:
            ```
            >>> list(Dice(4)._individual_dice_rolls())
            [[1, 2, 3, 4]]
            ```

            For 2d4 + d6 + 2:
            ```
            >>> from ttrpg_dice import d
            >>> dice = (2*d(4)) + d(6) + 2
            >>> list(dice._individual_dice_rolls())
            [[1], [1], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6]]
            ```
        """
        for faces, numdice in self.contents.items():
            yield from repeat(list(range(1, faces + 1)), numdice)

    @classmethod
    def _int(cls, other: SupportsInt, action: str, conjunction: str) -> int:
        """Attempts to convert `other` to an int for use in arithmetic magic methods."""
        try:
            other = int(other)
        except TypeError as e:
            msg = f"Cannot {action} '{type(other).__name__}' {conjunction} '{cls.__name__}'"
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
    """

    def __init__(self, dice: Dice) -> None:
        """
        Initialize the DiceIndexError for the given Dice object.

        Args:
            dice (Dice): The Dice object where the error occurred.
        """
        msg = f"Invalid side: This Dice has sides numbered 1 to {len(dice)}."
        super().__init__(msg)
