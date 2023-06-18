from ..utils import GameConfig
from .entity import Entity


class Background(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config, config.images.background)
