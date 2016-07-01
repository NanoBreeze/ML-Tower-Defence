import pygame
import path
import abc


class Ballon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""
    def __init__(self) :
        super().__init__()

        self.image = pygame.Surface([30, 30])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 50
        self.counter = 0 #this is used for iterating witht he path. This is a bad idea, might need a generator instead
        self.path = [(100, y) for y in range(50, 360)]

    @abc.abstractmethod
    def handle_pop(self):
        """Actions that happen when the ballon is popped"""
        pass


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

   def handle_pop(self):
      pass



