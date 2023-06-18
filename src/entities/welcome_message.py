from ..utils import GameConfig
from .entity import Entity


class WelcomeMessage(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config=config,
            image=config.images.message,
            x=int(
                (config.window.width - config.images.message.get_width()) / 2
            ),
            y=int(config.window.height * 0.12),
        )
