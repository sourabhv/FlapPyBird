from ..utils import GameConfig
from .entity import Entity


class Floor(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config, config.images.base, 0, config.window.viewport_height
        )
        self.vel_x = 4
        self.x_extra = (
            config.images.base.get_width()
            - config.images.background.get_width()
        )

    def stop(self) -> None:
        self.vel_x = 0

    def draw(self) -> None:
        self.x = -((-self.x + self.vel_x) % self.x_extra)
        super().draw()
