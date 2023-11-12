
import random
import time

from .game_result import GameScore

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
        super().__init__(config, random_y=random.randint(-1, 1))

        self.model = Model()
        
        self.score = GameScore(config)
        self.time_alive = 0
        self.fitness = 0

        self.is_alive = True
        
    def start_flying(self):
        self.time_alive = time.time()
    
    def stop_flying(self):
        self.set_alive(False)
        self.time_alive = time.time() - self.time_alive
    
    def set_alive(self, alive):
        self.is_alive = alive
    
    def get_alive(self):
        return self.is_alive
    
    def get_model_instance(self):
        return self.model
    
    def get_score(self):
        return self.score
    
    def calculate_fitness(self):
        """
        Calculates the fitness of a bird in the Flappy Bird game.

        The fitness is calculated as a weighted combination of the bird's score and time alive. The weights for the score
        and time alive can be adjusted to change the relative importance of each factor.

        """

        # Weights for the score and time alive
        # These values can be adjusted to change the relative importance of each factor
        weight_for_score = 1.0
        weight_for_time_alive = 1

        # Calculate the fitness as a weighted combination of the score and time alive
        score = self.score.get_game_score()
        self.fitness = (weight_for_score * score) + (weight_for_time_alive * self.time_alive)
        print(f"Fitness: {self.fitness}")
    
    def get_fitness(self):
        return self.fitness