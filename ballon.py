import pygame
import abc


class Ballon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""
    def __init__(self, colour, position, bounty=1, width = 30, height=30):
        assert isinstance(colour, tuple), "'colour' must be a tuple. It is currently a {}".format(type(colour))
        assert isinstance(position, tuple), "'pos' must be a tuple. It is currently a {}".format(type(position))

        super().__init__()

        #self._colour = colour
        #self._width = width
        #self._height = height
        #self._position = position
        #self._bounty = bounty #the amount of money earned when this ballon is popped

        self.image = pygame.Surface([30, 30])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    @abc.abstractmethod
    def handle_pop(self):
        """Actions that happen when the ballon is popped"""
        pass

    def update(self):
        pass

    def __str__(self):
        """Specifies the string name of this class"""
        return self.__class__.__name__



class BallonL1(Ballon):
   """First, and lowest, level of Ballon"""

   def handle_pop(self):
      pass



