
import time
from .game_result import GameResult
from .entities.player import Player
from .model import Model

class Bird(Player):
    """
    Represents the bird player in the Flappy Bird game.

    """
    def __init__(self, config) -> None:
        super().__init__(config)

        self.model = Model()
        self.score = 0
        self.time_alive = 0
        self.fitness = 0
        
    def start_flying(self):
        self.time_alive = time.time()

    def stop_flying(self):
        self.time_alive = time.time() - self.time_alive
    
    def reset_score(self) -> None:
        self.score = 0

    def add_score(self) -> None:
        self.score += 1

    def calculate_fitness(self):
        """
        Calculates the fitness of a bird in the Flappy Bird game.
        The fitness is calculated as a weighted combination of the bird's score and time alive. The weights for the score
        and time alive can be adjusted to change the relative importance of each factor.
        """

        # Weights for the score and time alive
        # These values can be adjusted to change the relative importance of each factor
        weight_for_score = 1.0
        weight_for_time_alive = 0.1

        # Calculate the fitness as a weighted combination of the score and time alive
        self.fitness = (weight_for_score * self.score) + (weight_for_time_alive * self.time_alive)
        print(f"Fitness: {self.fitness}")

    def get_fitness(self):
        return self.fitness
