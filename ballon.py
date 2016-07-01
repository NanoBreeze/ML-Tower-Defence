import pygame
import path
import abc


class Ballon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""
    def __init__(self, colour, position, path, bounty=1, width = 30, height=30):
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
        self.counter = 0 #this is used for iterating witht he path. This is a bad idea, might need a generator instead
        self.path = path
        print(self.path)

    @abc.abstractmethod
    def handle_pop(self):
        """Actions that happen when the ballon is popped"""
        pass


    def update(self):
        self.move()


    def move(self):
        try:
            self.rect.x = self.path[self.counter][0]
            self.rect.y = self.path[self.counter][1]
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



