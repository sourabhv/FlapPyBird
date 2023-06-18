from typing import Optional

import pygame

from ..utils import GameConfig, get_hit_mask, pixel_collision


class Entity:
    def __init__(
        self,
        config: GameConfig,
        image: Optional[pygame.Surface] = None,
        x=0,
        y=0,
        w: int = None,
        h: int = None,
        **kwargs,
    ) -> None:
        self.config = config
        self.image = image
        self.hit_mask = get_hit_mask(image) if image else None
        self.x = x
        self.y = y
        self.w = w or (image.get_width() if image else 0)
        self.h = h or (image.get_height() if image else 0)
        self.__dict__.update(kwargs)

    def update_image(
        self, image: pygame.Surface, w: int = None, h: int = None
    ) -> None:
        self.image = image
        self.hit_mask = get_hit_mask(image)
        self.w = w or (image.get_width() if image else 0)
        self.h = h or (image.get_height() if image else 0)

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def collide(self, other) -> bool:
        if not self.hit_mask or not other.hit_mask:
            return self.rect.colliderect(other.rect)
        return pixel_collision(
            self.rect, other.rect, self.hit_mask, other.hit_mask
        )

    def tick(self) -> None:
        self.draw()
        if self.config.debug:
            pygame.draw.rect(
                self.config.screen,
                (255, 0, 0),
                self.rect,
                1,
            )
            # write x and y at top of rect
            font = pygame.font.SysFont("Arial", 13, True)
            text = font.render(f"{self.x}, {self.y}", True, (255, 255, 255))
            self.config.screen.blit(
                text,
                (
                    self.x + self.w / 2 - text.get_width() / 2,
                    self.y - text.get_height(),
                ),
            )

    def draw(self) -> None:
        if self.image:
            self.config.screen.blit(self.image, (self.x, self.y))
