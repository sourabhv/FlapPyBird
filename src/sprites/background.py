from .sprite import Sprite


class Background(Sprite):
    def setup(self) -> None:
        self.x = 0
        self.y = 0

    def tick(self) -> None:
        self.screen.blit(self.images.background, (self.x, self.y))
