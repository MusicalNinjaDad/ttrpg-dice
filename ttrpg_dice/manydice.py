"""Rolling multiple dice."""

from __future__ import annotations

from collections.abc import Mapping
from itertools import zip_longest
from math import comb
from typing import TYPE_CHECKING

from matplotlib import pyplot as plt
from tabulate2 import tabulate

if TYPE_CHECKING:
    from collections.abc import Iterable

    from matplotlib.figure import Figure
    from mpl_toolkits.mplot3d.axes3d import Axes3D

    from .dice import Dice


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
    if target > dicetype:
        msg = f"Good luck rolling {target} on a d{dicetype}!"
        raise ValueError(msg)

    def _p(hits: int) -> float:
        """Calculates the probability of an exact number of hits."""
        misses = numdice - hits
        p_successes = (target / dicetype) ** hits
        p_fails = (1 - (target / dicetype)) ** (misses)
        return p_successes * p_fails * comb(numdice, hits)

    probs = [_p(hits) for hits in range(numdice + 1)]
    return [round(sum(probs[i:]) * dicetype) for i, _ in enumerate(probs)]


class LazyRollTable:
    """Table of values for lazyrolls of varying numbers of goblins."""

    def __init__(self, maxdice: int, dicetype: int, target: int) -> None:
        """Create a table of lazyrolls for up to `maxdice`."""
        self._maxdice = maxdice
        self._maxdicerange = range(maxdice + 1)
        """use to iterate from `0` to `maxdice` rolls `for i in self._maxdicerange`"""
        self._dicetype = dicetype
        self._target = target
        self.rolls = [lazyroll(i, dicetype, target) for i in self._maxdicerange]
        """List of lists of resulting lazyrolls - (0-indexed, so _includes_ 0 dice and 0 hits)"""

    def __eq__(self, value: object) -> bool:
        """Compare self.rolls if `value` is not another `LazyRollTable`."""
        if not isinstance(value, LazyRollTable):
            return self.rolls == value
        return self.rolls == value.rolls

    def __repr__(self) -> str:  # noqa: D105
        return f"LazyRollTable for up to {self._maxdice}d{self._dicetype} targeting {self._target}: {self.rolls}"

    def __str__(self) -> str:
        """Format as a nice table ignoring zero dice and zero hits."""
        tab = "\t"
        newline = "\n"

        def _formatroll(numdice: int, rolls: list[int]) -> str:
            lazytargets = tab.join(str(lazytarget) for lazytarget in rolls[1:])
            return tab.join([str(numdice), lazytargets])

        description = f"Lazyroll table for up to {self._maxdice}d{self._dicetype} targeting {self._target} for success:"
        table_header = f"\tHITS\n\t{tab.join(str(i) for i in self._maxdicerange[1:])}"
        table_lines = [_formatroll(d, r) for d, r in enumerate(self.rolls)]
        return newline.join([description, "", table_header, *table_lines[1:]])


class PoolComparison:
    """Comparison of related dicepools."""

    def __init__(self, pools: dict[str, Dice] | Iterable[Dice], outcomes: dict[str, slice]) -> None:
        """Create comparison based on dict of named pools and dict of named outcomes."""
        if isinstance(pools, Mapping):
            self.pools = pools
        else:
            self.pools = {pool: pool for pool in pools}
        self.outcomes = outcomes
        self.chances = {
            (pool, outcome): sum(die[index])
            for pool, die in self.pools.items()
            for outcome, index in self.outcomes.items()
        }
        """Dict of chances indexed by (pool, outcome)"""

    def __str__(self) -> str:
        """Nicely formatted table."""
        data = [[pool] + [self.chances[pool, outcome] * 100 for outcome in self.outcomes] for pool in self.pools]
        headers = ["pool", *self.outcomes]
        return tabulate(data, headers=headers, tablefmt="plain", floatfmt=".2f")

    def plot(self) -> tuple[Figure, Axes3D]:
        """Plot as a 3d Bar with matplotlib and return the Axes."""
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.bar3d(**self.plotable(), shade=True)
        ax.set_yticks([y + 0.5 for y, _ in enumerate(self.pools)], [str(pool) for pool in self.pools])
        ax.set_xticks([x + 0.5 for x, _ in enumerate(self.outcomes)], [str(outcome) for outcome in self.outcomes])
        return fig, ax

    def plotable(self) -> dict[str, list]:
        """Return bar location and sizes suitable for passing directly to matplotlib bar3d()."""
        x_locations = []
        y_locations = []
        z_locations = []
        dx_widths = []
        dy_widths = []
        dz_heights = []
        colours = []
        alphas = [
            0,  # -Z
            1,  # +Z (top)
            0,  # -Y
            0,  # +Y
            0.2,  # -X
            0.2,  # +X
        ]
        poolcolours = "bgrcmy"

        # Basic Colour Cycle (per pool)
        # ("b",0),("b",1),("b",0),("b",0),("b",0.2),("b",0.2),
        # ("g",0),("g",1),("g",0),("g",0),("g",0.2),("g",0.2),
        # ("r",0),("r",1),("r",0),("r",0),("r",0.2),("r",0.2),
        # ("c",0),("c",1),("c",0),("c",0),("c",0.2),("c",0.2),
        # ("m",0),("m",1),("m",0),("m",0),("m",0.2),("m",0.2),
        # ("y",0),("y",1),("y",0),("y",0),("y",0.2),("y",0.2),

        for x, outcome in enumerate(self.outcomes.keys()):
            for y, pool in enumerate(self.pools.keys()):
                x_locations.append(x)
                y_locations.append(y)
                z_locations.append(0)
                dx_widths.append(1)
                dy_widths.append(1)
                dz_heights.append(self.chances[(pool, outcome)])
                colours.extend(
                    zip_longest(poolcolours[y % len(poolcolours)], alphas, fillvalue=poolcolours[y % len(poolcolours)]),
                )

        return {
            "x": x_locations,
            "y": y_locations,
            "z": z_locations,
            "dx": dx_widths,
            "dy": dy_widths,
            "dz": dz_heights,
            "color": colours,
        }
