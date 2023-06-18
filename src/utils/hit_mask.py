from typing import List, Tuple

from .images import Images

# create custom type
HitMaskType = List[List[bool]]


class HitMask:
    pipe: Tuple[HitMaskType]
    player: Tuple[HitMaskType]

    def __init__(self, images: Images) -> None:
        # hit mask for pipe
        self.pipe = (
            self.make_hit_mask(images.pipe[0]),
            self.make_hit_mask(images.pipe[1]),
        )
        # hit mask for player
        self.player = (
            self.make_hit_mask(images.player[0]),
            self.make_hit_mask(images.player[1]),
            self.make_hit_mask(images.player[2]),
        )

    def make_hit_mask(self, image) -> HitMaskType:
        """returns a hit mask using an image's alpha."""
        return list(
            (
                list(
                    (
                        bool(image.get_at((x, y))[3])
                        for y in range(image.get_height())
                    )
                )
                for x in range(image.get_width())
            )
        )
