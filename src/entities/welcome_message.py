from ..utils import GameConfig
from .entity import Entity


class WelcomeMessage(Entity):
    def __init__(self, config: GameConfig) -> None:
        image = config.images.welcome_message
        super().__init__(
            config=config,
            image=image,
            x=(config.window.width - image.get_width()) // 2,
            y=int(config.window.height * 0.12),
        )
