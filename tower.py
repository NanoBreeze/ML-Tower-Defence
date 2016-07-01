import abc
import pygame
import pygame.surface
import pygame.sprite


class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""
    def __init__(self, position):
        assert isinstance(position, tuple), "'position' must be a two-element tuple. It is currently {}".format(type(position))
        super().__init__()
        self._position = position

        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        print('Update called')

    def handle_click(self):
        """Code executes when the user's mouse presses this tower"""
        pass




class LinearTower(Tower):
    """Attacks in a straight line"""
    pass

