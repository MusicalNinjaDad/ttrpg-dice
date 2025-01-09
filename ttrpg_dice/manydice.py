"""Rolling multiple dice."""

from math import comb


def multiroll(numdice: int, dicetype: int, target: int) -> list[int]:
    """Calculate equivalent single roll instead of rolling multiple dice."""
    def _p(hits: int) -> int:
        misses = numdice - hits
        p_successes = (target/dicetype) ** hits
        p_fails = (1-(target/dicetype)) ** (misses)
        p_hits = p_successes * p_fails * comb(numdice, hits)
        return round(p_hits * dicetype)
    probs = [_p(hits) for hits in range(numdice+1)]
    return [sum(probs[i:]) for i, _ in enumerate(probs)]