import abc
import pygame
import pygame.surface
import pygame.sprite

class DefaultAttackRange(pygame.sprite.Sprite):
    def __init__(self, position, group):
        assert isinstance(position, tuple), "'position' must be a two-element tuple. It is currently {}".format(type(position))
        super().__init__()
        self.image = pygame.Surface([150, 150])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.add(group)


class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""
    def __init__(self, position, DISPLAYSURF):
        assert isinstance(position, tuple), "'position' must be a two-element tuple. It is currently {}".format(type(position))
        super().__init__()
        self._position = position
        self.attack_range_group = pygame.sprite.Group()
        self.attack_range = DefaultAttackRange(position, self.attack_range_group)

        self.DISPLAYSURF = DISPLAYSURF
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.counter = 0 #just for testing the updating

    def update(self, ballon_group):
        self.attack_range_group.draw(self.DISPLAYSURF)
        hit = pygame.sprite.spritecollide(self.attack_range,ballon_group, False)
        for i in hit:
            print('Hit #{}'.format(self.counter))
            self.counter += 1

    def handle_click(self):
        """Code executes when the user's mouse presses this tower"""
        pass




class LinearTower(Tower):
    """Attacks in a straight line"""
    pass

