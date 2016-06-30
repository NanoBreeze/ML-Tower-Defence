import pygame
import abc


class Ballon(metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""
    def __init__(self, colour, pop_reward = 1, size = 30):
      self.colour = colour
      self.size = size
      self.pop_reward = pop_reward

    @abc.abstractmethod
    def handle_pop(self):
        """Actions that happen when the ballon is popped"""

    def __str__(self):
        """Specifies the string name of this class"""
        return self.__class__.__name__

    def __eq__(self, other):
        return type(self) is type(other)

class BallonL1(Ballon):
   """First, and lowest, level of Ballon"""

   def handle_pop(self):
      pass


class Parent():
   def __eq__(self, other):
      return type(self) is type(other)


class Child(Parent):
   pass

c = Child()
d = Child()
p = Parent()


b = BallonL1('red')
print(str(b))