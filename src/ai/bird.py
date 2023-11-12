
from .entities.player import Player
from .model import Model

class Bird(Player):
    """
    Represents the bird player in the Flappy Bird game.

    Attributes:
    - config (GameConfig): The game configuration.
    - random_y (int): The initial y position of the bird.
    - model (Model): The neural network model used to predict the bird's actions. (AKA: ADN)
    - fitness (Score): The score object used to track the bird's fitness.

    Methods:
    - get_model(self): Returns the neural network model used to predict the bird's actions.
    - get_fitness(self): Returns the score object used to track the bird's fitness.
    """
    def __init__(self, config) -> None:
        super().__init__(config)

        self.model = Model()
        