from enum import Enum

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from .game_observation import GameObservation


class GameAction(Enum):
    JUMP = 0
    DO_NOTHING = 1


class Model:
    def __init__(self) -> None:
        # Create a simple sequential model
        self.model = Sequential(
            [
                layers.Dense(
                    10, activation="relu", input_shape=(5,)
                ),  # Hidden layer with 10 neurons, and input shape of 5 (number of observation variables)
                layers.Dense(10, activation="relu"),  # Segunda capa oculta, opcional
                layers.Dense(
                    2, activation="softmax"
                ),  # Output layer with 2 neurons (number of actions)
            ]
        )

        # Compile the model with the Adam optimizer and a loss function for categorical outcomes
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

    # Decides action based on game observation
    def predict(self, game_observation: GameObservation) -> GameAction:
        # Preprocess observation into the format the model expects (a batch of one observation)
        observation = game_observation.as_vector().reshape(
            1, -1
        )  # Reshape the observation to be a batch of one
        # Get the model's prediction
        action_probabilities = self.model.predict(observation)
        # Determine the action based on the highest probability
        action = GameAction(np.argmax(action_probabilities[0]))

        return action
