import abc
import pygame
import pygame.surface
import pygame.sprite
import math
import bullet
import colours
import logging

logging.basicConfig(level=logging.DEBUG)

LINEAR_TOWER        = 'LINEAR_TOWER'
THREE_SIXTY_TOWER   = 'THREE_SIXTY_TOWER'
EXPLOSION_TOWER     = 'EXPLOSION_TOWER'
TELEPORTATION_TOWER = 'TELEPORTATION_TOWER'


class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""
    def __init__(self, colour, position, dimension, attack_radius, DISPLAYSURF):
        assert isinstance(colour, tuple), 'colour parameter must be a tuple instance'
        assert isinstance(position, tuple), 'position parameter must be a tuple instance'
        assert isinstance(dimension, tuple), 'dimension parameter must be a tuple instance'

        super().__init__()

        self.attack_radius = attack_radius

        self.DISPLAYSURF = DISPLAYSURF
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        pygame.draw.circle(DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), attack_radius, 1)

        self.attack_again_counter = 10 #just for testing the updating

    @abc.abstractmethod
    def update(self, ballon_sprites):
        pass

    def handle_click(self):
        """Code executes when the user's mouse presses this tower"""
        pass




class LinearTower(Tower):
    """Attacks in a straight line"""
    def __init__(self, DISPLAYSURF):
        super().__init__(colour=colours.YELLOW,
                         position=(150, 150),
                         dimension=(50, 50),
                         attack_radius=80,
                         DISPLAYSURF=DISPLAYSURF)

    def update(self, ballon_sprites, bullet_sprites):
        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self.attack_radius, 1)

        #possible to attack again
        if self.attack_again_counter == 10:

            #check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                #if within range, print and create a bullet
                    if math.hypot(ballon.rect.centerx - self.rect.centerx, ballon.rect.centery - self.rect.centery) <= self.attack_radius:
                        logging.debug('Detected. x distance: {0}, y distance:{1}'.format(ballon.rect.centerx - self.rect.centerx, ballon.rect.centery - self.rect.centery))
                        bullet_sprites.add(bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery), destination=(ballon.rect.centerx, ballon.rect.centery)))
                        self.attack_again_counter = 0
                        break
        else:
            self.attack_again_counter += 1



def create_tower(tower_type, DISPLAYSURF):
    if tower_type == LINEAR_TOWER:
        return LinearTower(DISPLAYSURF)
