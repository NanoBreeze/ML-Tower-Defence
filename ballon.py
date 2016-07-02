import colours
import pygame
import path
import abc

BALLON_L1 = 'BALLON_L1'
class Ballon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""
    def __init__(self, colour, position, dimension, path) :

        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.counter = 0 #this is used for iterating witht he path. This is a bad idea, might need a generator instead
        self.path = path



    def update(self, bullet_sprites):
        if pygame.sprite.spritecollide(self, bullet_sprites, True):
            self.kill()
        else:
            self.move()


    def move(self):
        try:
            self.rect.centerx = self.path[self.counter][0]
            self.rect.centery = self.path[self.counter][1]
            self.counter += 1
        except:
            pass



    def __str__(self):
        """Specifies the string name of this class"""
        return self.__class__.__name__



class BallonL1(Ballon):
   """First, and lowest, level of Ballon"""




def create_ballon(ballon_type, position, path):
    if ballon_type == BALLON_L1:
        return BallonL1(colours.RED, position, (30, 30), path)
