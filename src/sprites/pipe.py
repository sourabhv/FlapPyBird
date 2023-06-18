import random
from typing import List

from pygame import Surface

from .sprite import Sprite


class Pipe(Sprite):
    def setup(self) -> None:
        self.x = 0
        self.y = 0
        self.set_image(self.images.pipe[0])
        self.mid_x = self.x + self.images.pipe[0].get_width() / 2
        # TODO: make this change with game progress
        self.vel_x = -5

    def set_image(self, image: Surface) -> None:
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def tick(self) -> None:
        self.x += self.vel_x
        self.mid_x = self.x + self.images.pipe[0].get_width() / 2
        self.screen.blit(self.image, (self.x, self.y))


class Pipes(Sprite):
    upper: List[Pipe]
    lower: List[Pipe]

    def setup(self) -> None:
        # TODO: make this change with game progress
        self.pipe_gap = 120
        self.top = 0
        self.bottom = self.window.play_area_height
        self.reset()

    def reset(self) -> None:
        self.upper = []
        self.lower = []
        self.spawn_initial_pipes()

    def tick(self) -> None:
        if self.can_spawn_more():
            self.spawn_new_pipes()
        self.remove_old_pipes()

        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.tick()
            low_pipe.tick()

    def stop(self) -> None:
        for pipe in self.upper + self.lower:
            pipe.vel_x = 0

    def can_spawn_more(self) -> bool:
        # has 1 or 2 pipe and first pipe is almost about to exit the screen
        return 0 < len(self.upper) < 3 and 0 < self.upper[0].x < 5

    def spawn_new_pipes(self):
        # add new pipe when first pipe is about to touch left of screen
        upper, lower = self.make_random_pipes()
        self.upper.append(upper)
        self.lower.append(lower)

    def remove_old_pipes(self):
        # remove first pipe if its out of the screen
        if (
            len(self.upper) > 0
            and self.upper[0].x < -self.images.pipe[0].get_width()
        ):
            self.upper.pop(0)
            self.lower.pop(0)

    def spawn_initial_pipes(self):
        upper_1, lower_1 = self.make_random_pipes()
        upper_1.x = self.window.width + 100
        lower_1.x = self.window.width + 100

        upper_2, lower_2 = self.make_random_pipes()
        upper_2.x = self.window.width + 100 + (self.window.width / 2)
        lower_2.x = self.window.width + 100 + (self.window.width / 2)

        self.upper.append(upper_1)
        self.upper.append(upper_2)

        self.lower.append(lower_1)
        self.lower.append(lower_2)

    def make_random_pipes(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        base_y = self.window.play_area_height

        gap_y = random.randrange(0, int(base_y * 0.6 - self.pipe_gap))
        gap_y += int(base_y * 0.2)
        pipe_height = self.images.pipe[0].get_height()
        pipe_x = self.window.width + 10

        upper_pipe = Pipe(*self._args)
        upper_pipe.x = pipe_x
        upper_pipe.y = gap_y - pipe_height
        upper_pipe.set_image(self.images.pipe[0])

        lower_pipe = Pipe(*self._args)
        lower_pipe.x = pipe_x
        lower_pipe.y = gap_y + self.pipe_gap
        lower_pipe.set_image(self.images.pipe[1])

        return upper_pipe, lower_pipe
