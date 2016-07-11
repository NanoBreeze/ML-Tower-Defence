import abc
import pygame
import colours
import math
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

STANDARD_BULLET = 'STANDARD_BULLET'
EXPLOSION_BULLET = 'EXPLOSION_BULLET'
TELEPORTATION_BULLET = 'TELEPORTATION_BULLET'


class Bullet(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """
    Base class for all bullets
    """
    def __init__(self, start_position, end_position, pop_power, dimension=(10, 10), colour=colours.GREEN):
        """
        :param start_position: 2-element tuple, the starting position of this bullet
        :param end_position: 2-element tuple, the intended final position of this bullet
        :param pop_power: int, the number of layers to peel from the balloon if this bullet collides with it
        :param dimension: 2-element tuple, the size of this bullet
        :param colour: colours...., the colour of this bullet
        """
        assert isinstance(start_position, tuple) and len(start_position) == 2, 'start_position must be a 2-element tuple'
        assert isinstance(end_position, tuple) and len(end_position) == 2, 'end_position must be a 2-element tuple'
        assert isinstance(pop_power, int), 'pop_power must be an integer'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'dimension must be a 2-element tuple'
        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'

        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = start_position[0]
        self.rect.centery = start_position[1]

        self.destination_x = end_position[0]
        self.destination_y = end_position[1]

        self.pop_power = pop_power
        self.frames_remaining_until_self_destroy = math.hypot(self.destination_x - self.rect.centerx,
                                                              self.destination_y - self.rect.centery) / 20
        # logger.debug('self.destination_x: {}, self.rect.centerx: {}, self.destination_y: {}, self.rect.centery: {}, frames_remaining...: {}'.format(self.destination_x, self.rect.centerx, self.destination_y, self.rect.centery, self.frames_remaining_until_self_destroy))
        # step_x and step_y represents how many pixels the bullet moves in the x and y direction each frame
        self.step_x = (self.destination_x - self.rect.centerx) / self.frames_remaining_until_self_destroy
        self.step_y = (self.destination_y - self.rect.centery) / self.frames_remaining_until_self_destroy

    def update(self):
        """
        Called every frame. If the bullet is to continue moving, continue moving. If it has reached the end of its time (frames_remaining_until_self_destroy), kill self
        """
        if self.frames_remaining_until_self_destroy:
            # moves towards the destination by step size
            self.rect.centerx += self.step_x
            self.rect.centery += self.step_y
            self.frames_remaining_until_self_destroy -= 1
        else:
            # logger.info('the value of frames_remaining_until_... is: ' + str(self.frames_remaining_until_self_destroy))
            self.kill()

    @abc.abstractmethod
    def handle_collision_with_balloon(self):
        """What happens when this bullet hits a balloon"""
        pass


class StandardBullet(Bullet):
    def __init__(self, start_position, end_position, pop_power):
        """
        :param start_position: 2-element tuple, the starting position of this bullet
        :param end_position: 2-element tuple, the intended final position of this bullet
        :param pop_power: int, the number of layers to peel from the balloon this bullet makes contact with
        """
        assert isinstance(start_position, tuple) and len(start_position) == 2, 'start_position must be a 2-element tuple'
        assert isinstance(end_position, tuple) and len(end_position) == 2, 'end_position must be a 2-element tuple'
        assert isinstance(pop_power, int), 'pop_power must be an integer'

        super().__init__(start_position, end_position, pop_power)

    def handle_collision_with_balloon(self):
        """If this bullet hits a balloon, destroy this bullet"""
        self.kill()


class ExplosionBullet(Bullet):
    def __init__(self, start_position, end_position, pop_power):
        """
        :param start_position: 2-element tuple, the starting position of this bullet
        :param end_position: 2-element tuple, the intended final position of this bullet
        :param pop_power: int, the number of layers to peel from the balloon this bullet makes contact with
        """
        assert isinstance(start_position, tuple) and len(start_position) == 2, 'start_position must be a 2-element tuple'
        assert isinstance(end_position, tuple) and len(end_position) == 2, 'end_position must be a 2-element tuple'
        assert isinstance(pop_power, int), 'pop_power must be an integer'

        super().__init__(start_position, end_position, pop_power)

    def handle_collision_with_balloon(self, bullet_sprites):
        """
        :param bullet_sprites: pygame.sprite.Group, contains all the bulleti sprites in the game
        Upon hitting a balloon, 4 Standard bullets are created from the position of this one. Then this one is destroyed
        """
        bullet_sprites.add(
            create_bullet(bullet_type=STANDARD_BULLET,
                          start=(self.rect.centerx, self.rect.centery),
                          destination=(self.rect.centerx, self.rect.centery - 20),
                          pop_power=self.pop_power),
            create_bullet(bullet_type=STANDARD_BULLET,
                          start=(self.rect.centerx, self.rect.centery),
                          destination=(self.rect.centerx + 20, self.rect.centery),
                          pop_power=self.pop_power),
            create_bullet(bullet_type=STANDARD_BULLET,
                          start=(self.rect.centerx, self.rect.centery),
                          destination=(self.rect.centerx, self.rect.centery + 20),
                          pop_power=self.pop_power),
            create_bullet(bullet_type=STANDARD_BULLET,
                          start=(self.rect.centerx, self.rect.centery),
                          destination=(self.rect.centerx - 20, self.rect.centery),
                          pop_power=self.pop_power),
        )
        self.kill()


class TeleportationBullet(Bullet):
    def __init__(self, start_position, end_position, pop_power):
        """
        :param start_position: 2-element tuple, the starting position of this bullet
        :param end_position: 2-element tuple, the intended final position of this bullet
        :param pop_power: int, the number of layers to peel from the balloon this bullet makes contact with
        """

        assert isinstance(start_position, tuple) and len(start_position) == 2, 'start_position must be a 2-element tuple'
        assert isinstance(end_position, tuple) and len(end_position) == 2, 'end_position must be a 2-element tuple'
        assert isinstance(pop_power, int), 'pop_power must be an integer'

        super().__init__(start_position, end_position, pop_power)

    def handle_collision_with_balloon(self):
        """Destroy this bullet upon collision with a balloon"""
        self.kill()


def create_bullet(bullet_type, start, destination, pop_power):
    """
    :param bullet_type: str constant, which balloon will be the current starting balloon for this context
    :param start: 2-element tuple, the start position of the bullet
    :param destination: 2-element tuple, the position the bullet is headed
    :param pop_power: int, the number of layer of balloon this bullet can pop if it hits a balloon
    :return: the bullet type, eg StandardBullet
    This simple factory creates a StandardBullet, ExplosionBullet, or TeleportationBullet
    """
    assert isinstance(bullet_type, str), 'bullet_type must be a string'
    assert isinstance(start, tuple) and len(start) == 2, 'start must be a 2-element tuple'
    assert isinstance(destination, tuple) and len(destination) == 2, 'destination must be a 2-element tuple'
    assert isinstance(pop_power, int), 'pop_power must be an integer'

    if bullet_type == STANDARD_BULLET:
        return StandardBullet(start, destination, pop_power)
    elif bullet_type == EXPLOSION_BULLET:
        return ExplosionBullet(start, destination, pop_power)
    elif bullet_type == TELEPORTATION_BULLET:
        return TeleportationBullet(start, destination, pop_power)

    raise NotImplementedError('the specified Bullet type is invalid')
