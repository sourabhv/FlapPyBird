
from .entities.player import Player
from .model import Model

class Bird(Player):
    """
    Represents the bird player in the Flappy Bird game.

    """
    def __init__(self, config) -> None:
        super().__init__(config)

        self.model = Model()
        