import colours
import pygame
import path
import abc
import logging
import logging.config
import bullet
import bank
import life_point

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')

BALLOON_L1 = 'BALLOON_L1'
BALLOON_L2 = 'BALLOON_L2'
BALLOON_L3 = 'BALLOON_L3'
BALLOON_L4 = 'BALLOON_L4'
BALLOON_L5 = 'BALLOON_L5'


class Balloon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""

    def __init__(self, colour, dimension, path_to_move, bounty=20, path_indexer=0):
        """
        :param colour: 4-element tuple, colour of the balloon
        :param dimension: 2-element tuple, size of the balloon
        :param path_to_move: path.Path, the predetermined path this balloon will move on
        :param bounty: int, the amount of money awarded for popping this ballon
        :param path_indexer: int, the index on the path that this balloon is on
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'dimension must be a 2-element tuple'
        assert isinstance(path_to_move, path.Path), 'path_to_move must a Path object'
        assert isinstance(bounty, int), 'bounty must be an integer'
        assert isinstance(path_indexer, int), 'path_indexer must be an integer'

        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.path_index = path_indexer  # this is used for iterating which tuple of the path_to_move to move to. Very useful with teleportation
        self.rect.centerx = path_to_move[self.path_index][0]
        self.rect.centery = path_to_move[self.path_index][1]
        self.path = path_to_move
        self.bounty = bounty

    def update(self, bullet_sprites):
        """
        :param bullet_sprites: pygame.sprite.Group, contains all the bullet sprites in the game
        :return: if hit by bullet, depending on its type, either returns the pop power of the collided bullet or teleports itself. If not hit by bullet, moves
        Checks if this balloon is hit by bullets or not. If not hit, move. If hit, return a value
        """

        assert isinstance(bullet_sprites, pygame.sprite.Group), 'bullet_sprites must be a pygame.sprite.Group type'

        #this is redundant, already checked in the context
        collided_bullets = pygame.sprite.spritecollide(self, bullet_sprites, False)
        if collided_bullets:
            for collided_bullet in collided_bullets:
                if isinstance(collided_bullet, bullet.StandardBullet):
                    # logger.debug('=================== STANDARD BULLET=======================')
                    collided_bullet.handle_ballon_collision()
                    return collided_bullet.pop_power  # represents should handle pop
                elif isinstance(collided_bullet, bullet.ExplosionBullet):
                    # logger.debug('=================== EXPLOSION BULLET=======================')
                    # explosion bullet will create more bullets
                    collided_bullet.handle_ballon_collision(bullet_sprites)
                    return collided_bullet.pop_power  # represents should handle pop
                elif isinstance(collided_bullet, bullet.TeleportationBullet):
                    # logger.debug('=================== TELEPORTATION BULLET=======================')
                    collided_bullet.handle_ballon_collision()
                    self.teleport()
                    return False  # represents don't hanlde pop. This ballon is being teleported
                raise NotImplementedError('the collided_bullet type is not allowed!')

    def move(self):
        """
        :return boolean, represents if the balloon has reached the end and thus, kills itself. Thus, the context can appropriately handle the case
        Increments the path_index so that the balloon progresses to the next point on the path
        """

        assert self.path_index <= len(self.path), 'the path_index must be less than the length of the path points list'
        if self.path_index == len(self.path) - 1:
            life_point.decrease()
            self.kill()
            return True
        else:
            self.rect.centerx = self.path[self.path_index][0]
            self.rect.centery = self.path[self.path_index][1]
            self.path_index += 1
            return False

    def teleport(self, back_track_path_indexer=20):
        """
        :param back_track_path_indexer: int, indicates the number of indices to move backwards from the current path_index on the path
        Teleports ballon back a certain number of indices on its path
        """

        assert isinstance(back_track_path_indexer, int), 'back_track_path_indexer must be an int'
        if back_track_path_indexer > self.path_index:
            self.path_index = 0
        else:
            self.path_index -= back_track_path_indexer


class BalloonL1(Balloon):
    """First, and lowest, level of Balloon"""

    def peel_layer(self):
        """
        :return: None, represents no more layer beneath this layer
        In BalloonL1, the lowest balloon layer, indicate that there are no other layers to return
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """

        return None  # there is no layer to return


class BalloonL2(Balloon):
    def peel_layer(self):
        """
        :return: BalloonL1, the layer underneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """

        return create_balloon(BALLOON_L1, self.path, self.path_index)


class BalloonL3(Balloon):
    def peel_layer(self):
        """
        :return: BalloonL2, the layer beneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon(BALLOON_L2, self.path, self.path_index)


class BalloonL4(Balloon):
    def peel_layer(self):
        """
        :return: BalloonL3, the layer beneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon(BALLOON_L3, self.path, self.path_index)


class BalloonL5(Balloon):
    def peel_layer(self):
        """
        :return: BalloonL2, the layer beneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon(BALLOON_L4, self.path, self.path_index)


class BalloonContext(Balloon):
    def __init__(self, current_ballon):
        """
        :param current_ballon: Balloon, the current balloon to store in this context object
        This is the context object for a state machine. The states are the level of balloon, and transitions between states represents peeling layers off a balloon
        """

        assert isinstance(current_ballon, Balloon), 'current_ballon must be a Balloon type'

        pygame.sprite.Sprite.__init__(self)
        self.current_ballon = current_ballon

    def update(self, bullet_sprites):
        """
        :param bullet_sprites: pygame.sprite.Group, contains all the bullets in the game
        Update(...) is called every frame and checks if the current_balloon is hit by bullet or not
        """

        assert isinstance(bullet_sprites, pygame.sprite.Group)
        #different ways to update, can move or handle is hit
        if pygame.sprite.spritecollide(self.current_ballon, bullet_sprites, False):
            # if layers_to_peel is a number, then the balloon is to be popped and the number of layers (of layers_to_peel) is to be peeled
            layers_to_peel = self.current_ballon.update(bullet_sprites)
            if layers_to_peel:
                self.handle_pop(layers_to_peel)
        else:
            self.move()

    def move(self):
        is_current_balloon_reached_end = self.current_ballon.move()
        if is_current_balloon_reached_end:
            self.kill()


    def handle_pop(self, layers_to_peel):
        """
        :param layers_to_peel: int, the number of layers (state transitions) to take off from the current balloon
        Statements that execute when this balloon is to be popped/layers away
        """

        assert isinstance(layers_to_peel, int)

        # logger.debug('inside BallonContext handle_pop()')
        for layer in range(layers_to_peel):
            # it's import to deposit here so that every deposit is made before the current ballon changes
            bank.deposit(self.current_ballon.bounty)
            self.current_ballon = self.current_ballon.peel_layer()
            if self.current_ballon is None:
                self.kill()
                break

    def get_centerX(self):
        """
        :return: the centerx of the current_balloon
        This is the equivalent of a getter
        """
        return self.current_ballon.rect.centerx

    def get_centerY(self):
        """
        :return: the centery of the current_balloon
         This si the equivalent for a getter
        """
        return self.current_ballon.rect.centery


def create_balloon(balloon_type, path_to_move_on, path_indexer=0):
    """
    :param balloon_type: str constant, which balloon to make (L1, L2, etc.)
    :param path_to_move_on: path.Path, the path this balloon is to take
    :param path_indexer: int, the index on the path to make the new balloon
    :return: various BalloonLX
    Simple factory for returning new balloons and is particularly used by individual balloons to indicate the next balloon layer, for state changing
    """

    assert isinstance(balloon_type, str), 'balloon_type must be a string'
    assert isinstance(path_to_move_on, path.Path), 'path_to_move_on must be a path_to_move_on type'
    assert isinstance(path_indexer, int), 'path_indexer must be an integer'

    if balloon_type == BALLOON_L1:
        return BalloonL1(colours.RED, (30, 30), path_to_move_on, 10, path_indexer)
    elif balloon_type == BALLOON_L2:
        return BalloonL2(colours.ORANGE, (30, 30), path_to_move_on, 20, path_indexer)
    elif balloon_type == BALLOON_L3:
        return BalloonL3(colours.YELLOW, (30, 30), path_to_move_on, 30, path_indexer)
    elif balloon_type == BALLOON_L4:
        return BalloonL4(colours.GREEN, (30, 30), path_to_move_on, 40, path_indexer)
    elif balloon_type == BALLOON_L5:
        return BalloonL5(colours.BLUE, (30, 30), path_to_move_on, 50, path_indexer)

    raise NotImplementedError('Not implemented yet!')


def create_balloon_context(balloon_type, path_to_move_on, path_indexer=0):
    """
    :param balloon_type: str constant, which balloon will be the current starting balloon for this context
    :param path_to_move_on: the path the balloon moves on
    :param path_indexer: the starting index on the path to move on
    :return: BalloonContext, composing with a balloon
    Simple factory for creating the encapsulated balloon. Internally, composed of LX balloons
    """

    assert isinstance(balloon_type, str), 'balloon_type must be a string'
    assert isinstance(path_to_move_on, path.Path), 'path_to_move_on must be a path_to_move_on type'
    assert isinstance(path_indexer, int), 'path_indexer must be an integer'

    balloon = create_balloon(balloon_type, path_to_move_on, path_indexer)
    return BalloonContext(balloon)
