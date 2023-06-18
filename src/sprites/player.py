from enum import Enum
from itertools import cycle

import pygame

from ..utils import clamp, pixel_collision
from .floor import Floor
from .pipe import Pipe, Pipes
from .sprite import Sprite


class PlayerMode(Enum):
    SHM = "SHM"
    NORMAL = "NORMAL"
    CRASH = "CRASH"


class Player(Sprite):
    def setup(self) -> None:
        self.img_idx = 0
        self.img_gen = cycle([0, 1, 2, 1])
        self.frame = 0
        self.crashed = False
        self.crash_entity = None
        self.width = self.images.player[0].get_width()
        self.height = self.images.player[0].get_height()
        self.reset_pos()
        self.set_mode(PlayerMode.SHM)

    def set_mode(self, mode: PlayerMode) -> None:
        self.mode = mode
        if mode == PlayerMode.NORMAL:
            self.reset_vals_normal()
            self.sounds.wing.play()
        elif mode == PlayerMode.SHM:
            self.reset_vals_shm()
        elif mode == PlayerMode.CRASH:
            self.sounds.hit.play()
            if self.crash_entity == "pipe":
                self.sounds.die.play()
            self.reset_vals_crash()

    def reset_pos(self) -> None:
        self.x = int(self.window.width * 0.2)
        self.y = int(
            (self.window.height - self.images.player[0].get_height()) / 2
        )
        self.mid_x = self.x + self.width / 2
        self.mid_y = self.y + self.height / 2

    def reset_vals_normal(self) -> None:
        self.vel_y = -9  # player's velocity along Y axis
        self.max_vel_y = 10  # max vel along Y, max descend speed
        self.min_vel_y = -8  # min vel along Y, max ascend speed
        self.acc_y = 1  # players downward acceleration

        self.rot = 45  # player's current rotation
        self.vel_rot = -3  # player's rotation speed
        self.rot_min = -90  # player's min rotation angle
        self.rot_max = 20  # player's max rotation angle

        self.flap_acc = -9  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_shm(self) -> None:
        self.vel_y = 1  # player's velocity along Y axis
        self.max_vel_y = 4  # max vel along Y, max descend speed
        self.min_vel_y = -4  # min vel along Y, max ascend speed
        self.acc_y = 0.5  # players downward acceleration

        self.rot = 0  # player's current rotation
        self.vel_rot = 0  # player's rotation speed
        self.rot_min = 0  # player's min rotation angle
        self.rot_max = 0  # player's max rotation angle

        self.flap_acc = 0  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_crash(self) -> None:
        self.acc_y = 2
        self.vel_y = 7
        self.max_vel_y = 15

    def update_img_idx(self):
        self.frame += 1
        if self.frame % 5 == 0:
            self.img_idx = next(self.img_gen)

    def tick_shm(self) -> None:
        if self.vel_y >= self.max_vel_y or self.vel_y <= self.min_vel_y:
            self.acc_y *= -1
        self.vel_y += self.acc_y
        self.y += self.vel_y

        self.mid_x = self.x + self.width / 2
        self.mid_y = self.y + self.height / 2

    def tick_normal(self) -> None:
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False

        self.y += min(
            self.vel_y, self.window.play_area_height - self.y - self.height
        )

        self.mid_x = self.x + self.width / 2
        self.mid_y = self.y + self.height / 2

    def tick_crash(self) -> None:
        if self.y + self.height < self.window.play_area_height - 1:
            self.y += min(
                self.vel_y, self.window.play_area_height - self.y - self.height
            )

        # player velocity change
        if self.vel_y < self.max_vel_y:
            self.vel_y += self.acc_y

        # rotate only when it's a pipe crash
        if self.crash_entity != "floor":
            self.rotate()

    def rotate(self) -> None:
        self.rot = clamp(self.rot + self.vel_rot, self.rot_min, self.rot_max)

    def tick(self) -> None:
        self.update_img_idx()
        if self.mode == PlayerMode.SHM:
            self.tick_shm()
        elif self.mode == PlayerMode.NORMAL:
            self.tick_normal()
            self.rotate()
        elif self.mode == PlayerMode.CRASH:
            self.tick_crash()

        self.draw_player()

    def draw_player(self) -> None:
        player_surface = pygame.transform.rotate(
            self.images.player[self.img_idx], self.rot
        )
        self.screen.blit(player_surface, (self.x, self.y))

    def flap(self) -> None:
        self.vel_y = self.flap_acc
        self.flapped = True
        self.rot = 45
        self.sounds.wing.play()

    def crossed(self, pipe: Pipe) -> bool:
        return pipe.mid_x <= self.mid_x < pipe.mid_x + 4

    def collided(self, pipes: Pipes, floor: Floor) -> bool:
        """returns True if player collides with base or pipes."""

        # if player crashes into ground
        if self.y + self.height >= floor.y - 1:
            self.crashed = True
            self.crash_entity = "floor"
            return True
        else:
            p_rect = pygame.Rect(self.x, self.y, self.width, self.height)

            for u_pipe, l_pipe in zip(pipes.upper, pipes.lower):
                # upper and lower pipe rects
                u_pipe_rect = pygame.Rect(
                    u_pipe.x, u_pipe.y, u_pipe.width, u_pipe.height
                )
                l_pipe_rect = pygame.Rect(
                    l_pipe.x, l_pipe.y, l_pipe.width, l_pipe.height
                )

                # player and upper/lower pipe hitmasks
                p_hit_mask = self.hit_mask.player[self.img_idx]
                u_hit_mask = self.hit_mask.pipe[0]
                l_hit_mask = self.hit_mask.pipe[1]

                # if bird collided with upipe or lpipe
                u_collide = pixel_collision(
                    p_rect, u_pipe_rect, p_hit_mask, u_hit_mask
                )
                l_collide = pixel_collision(
                    p_rect, l_pipe_rect, p_hit_mask, l_hit_mask
                )

                if u_collide or l_collide:
                    self.crashed = True
                    self.crash_entity = "pipe"
                    return True

            return False
