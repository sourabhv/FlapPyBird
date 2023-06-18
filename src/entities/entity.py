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
        self.x = x
        self.y = y
        if w or h:
            self.w = w or config.window.ratio * h
            self.h = h or w / config.window.ratio
            self.image = pygame.transform.scale(image, (self.w, self.h))
        else:
            self.image = image
            self.w = image.get_width() if image else 0
            self.h = image.get_height() if image else 0

        self.hit_mask = get_hit_mask(image) if image else None
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
        rect = self.rect
        if self.config.debug:
            pygame.draw.rect(self.config.screen, (255, 0, 0), rect, 1)
            # write x and y at top of rect
            font = pygame.font.SysFont("Arial", 13, True)
            text = font.render(
                f"{self.x:.1f}, {self.y:.1f}, {self.w:.1f}, {self.h:.1f}",
                True,
                (255, 255, 255),
            )
            self.config.screen.blit(
                text,
                (
                    rect.x + rect.w / 2 - text.get_width() / 2,
                    rect.y - text.get_height(),
                ),
            )

    def draw(self) -> None:
        if self.image:
            self.config.screen.blit(self.image, self.rect)
