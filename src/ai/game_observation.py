import numpy as np


class GameObservation:
    def __init__(
        self,
        bird_y_pos: int,
        y_dist_to_bot_pipe: int,
        y_dist_to_top_pipe: int,
        x_dist_to_pipe_pair: int,
        bird_y_vel: int,
    ) -> None:
        self.bird_y_pos = bird_y_pos
        self.y_dist_to_bot_pipe = y_dist_to_bot_pipe
        self.y_dist_to_top_pipe = y_dist_to_top_pipe
        self.x_dist_to_pipe_pair = x_dist_to_pipe_pair
        self.bird_y_vel = bird_y_vel

    def as_vector(self) -> np.ndarray:
        return np.array(
            [
                [
                    self.bird_y_pos,
                    self.y_dist_to_bot_pipe,
                    self.y_dist_to_top_pipe,
                    self.x_dist_to_pipe_pair,
                    self.bird_y_vel,
                ]
            ]
        )
