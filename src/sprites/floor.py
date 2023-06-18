from .sprite import Sprite


class Floor(Sprite):
    def setup(self) -> None:
        self.x = 0
        self.y = self.window.play_area_height
        # amount to shift on each tick
        self.vel_x = 4
        # amount by which floor can maximum shift to left
        self.x_extra = (
            self.images.base.get_width() - self.images.background.get_width()
        )

    def stop(self) -> None:
        self.vel_x = 0

    def tick(self) -> None:
        self.x = -((-self.x + self.vel_x) % self.x_extra)
        self.screen.blit(self.images.base, (self.x, self.y))
