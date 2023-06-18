from .sprite import Sprite


class GameOver(Sprite):
    def setup(self) -> None:
        self.x = int((self.window.width - self.images.gameover.get_width()) / 2)
        self.y = int(self.window.height * 0.2)

    def tick(self) -> None:
        self.screen.blit(self.images.gameover, (self.x, self.y))
