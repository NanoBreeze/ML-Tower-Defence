import abc
import pygame
import pygame.surface
import pygame.sprite
import math
import bullet




class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""
    def __init__(self, DISPLAYSURF):
        super().__init__()
        #self.attack_range_group = pygame.sprite.Group()
        #self.attack_range = DefaultAttackRange(position, self.attack_range_group)

        self.DISPLAYSURF = DISPLAYSURF
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 150
        self.rect.centery = 150
        self.r = pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (150, 150), 80, 1)

        self.wait_counter = 10 #just for testing the updating

    def update(self, ballon_sprites):
        self.r = pygame.draw.circle(self.DISPLAYSURF, (255, 255, 255), (150, 150), 80, 1)
        #check if any ballons are within the range of the circle, which is currently set to 80
        for ballon in ballon_sprites:
            #if within range, print and create a bullet
            if math.hypot(ballon.rect.centerx - 150, ballon.rect.centery - 150) <= 80:
                print('Detected. x distance: {0}, y distance:{1}'.format(ballon.rect.centerx - 150, ballon.rect.centery - 150))
                if self.wait_counter == 10:
                    b = bullet.Bullet((self.rect.x, self.rect.y), (ballon.rect.centerx, ballon.rect.centery))
                    self.wait_counter = 0
                else:
                    self.wait_counter += 1

    def handle_click(self):
        """Code executes when the user's mouse presses this tower"""
        pass




class LinearTower(Tower):
    """Attacks in a straight line"""
    pass

