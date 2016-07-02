import abc
import pygame
import colours
import sprite_groups
import math

STANDARD_BULLET = 'STANDARD_BULLET'

class Bullet(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    def __init__(self, start, destination, dimension=(10, 10), colour=colours.GREEN):
        super().__init__()
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.destination_x = destination[0]
        self.destination_y = destination[1]

        #step_x and step_y represents how far the bullet goes each frame
        self.frame_to_hit_Ballon = math.hypot(self.destination_x - self.rect.centerx, self.destination_y - self.rect.centery) / 20
        self.step_x = (self.destination_x - self.rect.centerx)/self.frame_to_hit_Ballon
        self.step_y = (self.destination_y - self.rect.centery)/self.frame_to_hit_Ballon
        sprite_groups.bullet_sprites.add(self)

    def update(self):
        #moves towards the destination by step size
        self.rect.centerx += self.step_x
        self.rect.centery += self.step_y

    


class StandardBullet(Bullet):
    def __init__(self, start, destination):
        assert isinstance(start, tuple), 'start must be a tuple'
        assert isinstance(destination, tuple), 'destination must be a tuple'

        super().__init__(start, destination)


def create_bullet(bullet_type, start, destination):
    if bullet_type == STANDARD_BULLET:
        return StandardBullet(start, destination)
