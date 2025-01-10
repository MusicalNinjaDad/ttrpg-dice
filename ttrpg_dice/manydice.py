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
    def _p(hits: int) -> int:
        misses = numdice - hits
        p_successes = (target/dicetype) ** hits
        p_fails = (1-(target/dicetype)) ** (misses)
        return p_successes * p_fails * comb(numdice, hits)
    probs = [_p(hits) for hits in range(numdice+1)]
    return [round(sum(probs[i:]) * dicetype) for i, _ in enumerate(probs)]