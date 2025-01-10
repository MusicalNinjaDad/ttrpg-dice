"""Rolling multiple dice."""

from math import comb


def lazyroll(numdice: int, dicetype: int, target: int) -> list[int]:
    """
    Calculate equivalent single roll instead of rolling multiple dice targetting the same success value.
    
    Arguments:
        numdice: the number of identical dice to roll
        dicetype: the number of faces on the dice to roll
        target: the target for a successful test

    Examples:
        Instead of rolling 4d100 to see which of your (skilled) goblins hit your party with their arrows you can use:
        ```
        >>> from ttrpg_dice import lazyroll
        >>> lazyroll (4, 100, 33)
        [100, 80, 40, 11, 1]
        ```
        Then roll 1d100 and interpret the hits:
        ```
        81-100:  0 hits
         41-80:  1 hit
         12-40:  2 hits
          2-11:  3 hits
             1:  4 hits
        ```
    """
    def _p(hits: int) -> float:
        """Calculates the probability of an exact number of hits."""
        misses = numdice - hits
        p_successes = (target/dicetype) ** hits
        p_fails = (1-(target/dicetype)) ** (misses)
        return p_successes * p_fails * comb(numdice, hits)
    probs = [_p(hits) for hits in range(numdice+1)]
    return [round(sum(probs[i:]) * dicetype) for i, _ in enumerate(probs)]

class LazyRollTable:    
    """Table of values for lazyrolls of varying numbers of goblins."""

    def __init__(self, maxdice: int, dicetype: int, target: int) -> None:
        """Create a table of lazyrolls for up to `maxdice`."""
        self._maxdice = maxdice
        self._maxdicerange = range(maxdice+1)
        """use to iterate from `0` to `maxdice` rolls `for i in self._maxdicerange`"""
        self._dicetype = dicetype
        self._target = target
        self.rolls = [lazyroll(i, dicetype, target) for i in self._maxdicerange]
        """List of lists of resulting lazyrolls - (0-indexed, so _includes_ 0 dice and 0 hits)"""

    def __eq__(self, value: object) -> bool:
        """Compare self.rolls if `value` is not another `LazyRollTable`."""
        if not isinstance(value, LazyRollTable):
            return self.rolls == value
        return self == value
    
    def __repr__(self) -> str:  # noqa: D105
        return f"LazyRollTable for up to {self._maxdice}d{self._dicetype} targeting {self._target}: {self.rolls}"
    
    def __str__(self) -> str:
        """Format as a nice table ignoring zero dice and zero hits."""
        tab = "\t"
        newline = "\n"
        def _formatroll(numdice: int, rolls: list[int]) -> str:
            lazytargets = tab.join(str(lazytarget) for lazytarget in rolls[1:])
            return tab.join([str(numdice),lazytargets])
        description = f"Lazyroll table for up to {self._maxdice}d{self._dicetype} targeting {self._target} for success:"
        table_header = f"\tHITS\n\t{tab.join(str(i) for i in self._maxdicerange[1:])}"
        table_lines = [_formatroll(d, r) for d, r in enumerate(self.rolls)]
        return newline.join([description,"",table_header, *table_lines[1:]])
