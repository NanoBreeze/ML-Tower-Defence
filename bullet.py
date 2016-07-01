import pygame
import sprite_groups
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start, destination):
        assert isinstance(start, tuple), 'position must be a tuple'
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.destination_x = destination[0]
        self.destination_y = destination[1]
        #step_x and step_y represents how far the bullet goes each frame

        self.frames_until_target = math.hypot(self.destination_x - self.rect.centerx, self.destination_y - self.rect.centery)/20
        self.step_x = (self.destination_x - self.rect.centerx)/self.frames_until_target
        self.step_y = (self.destination_y - self.rect.centery)/self.frames_until_target
        sprite_groups.bullet_sprites.add(self)

    def update(self):
        #moves towards the destination by step size
        self.rect.centerx += self.step_x
        self.rect.centery += self.step_y
