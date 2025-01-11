"""A Dice class."""

class Dice:
    """A Dice class."""

    def __init__(self, faces: int) -> None:
        """Build a die."""
        self.probabilities = [None] + faces*[1/faces]