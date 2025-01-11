"""A Dice class."""

class Dice:
    """A Dice class."""

    def __init__(self, faces: int) -> None:
        """Build a die."""
        self.probabilities = [None] + faces*[1/faces]
        """List of P(result) where result is index of list. P(0) = `None`"""
