from .sprite import Sprite


class WelcomeMessage(Sprite):
    def setup(self) -> None:
        self.x = int((self.window.width - self.images.message.get_width()) / 2)
        self.y = int(self.window.height * 0.12)

    def tick(self) -> None:
        self.screen.blit(self.images.message, (self.x, self.y))
