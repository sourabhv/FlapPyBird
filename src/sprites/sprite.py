import pygame

from ..utils.hit_mask import HitMask
from ..utils.images import Images
from ..utils.sounds import Sounds
from ..utils.window import Window


class Sprite:
    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int,
        window: Window,
        images: Images,
        sounds: Sounds,
        hit_mask: HitMask,
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.window = window
        self.images = images
        self.sounds = sounds
        self.hit_mask = hit_mask
        self._args = (
            self.screen,
            self.clock,
            self.fps,
            self.window,
            self.images,
            self.sounds,
            self.hit_mask,
        )

        self.setup()

    def setup(self) -> None:
        pass

    def tick() -> None:
        pass
