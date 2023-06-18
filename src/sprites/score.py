from .sprite import Sprite


class Score(Sprite):
    def setup(self) -> None:
        self.score = 0

    def reset(self) -> None:
        self.score = 0

    def add(self) -> None:
        self.score += 1
        self.sounds.point.play()

    def tick(self) -> None:
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(self.score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += self.images.numbers[digit].get_width()

        x_offset = (self.window.width - totalWidth) / 2

        for digit in scoreDigits:
            self.screen.blit(
                self.images.numbers[digit],
                (x_offset, self.window.height * 0.1),
            )
            x_offset += self.images.numbers[digit].get_width()
