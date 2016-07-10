import colours
import pygame
import path
import abc
import logging.config
import bullet
import bank
import life_point

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

BALLOON_L1 = 'BALLOON_L1'
BALLOON_L2 = 'BALLOON_L2'
BALLOON_L3 = 'BALLOON_L3'
BALLOON_L4 = 'BALLOON_L4'
BALLOON_L5 = 'BALLOON_L5'


class BalloonState(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""

    def __init__(self, colour, dimension, start_position, bounty=20):
        """
        :param colour: 4-element tuple, colour of the balloon
        :param dimension: 2-element tuple, size of the balloon
        :param start_position: 2-element tuple, the start position of the balloon
        :param bounty: int, the amount of money awarded for popping this ballon
        """
        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'dimension must be a 2-element tuple'
        assert isinstance(start_position, tuple) and len(start_position) == 2, 'path_to_move must a Path object'
        assert isinstance(bounty, int), 'bounty must be an integer'

        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = start_position[0]
        self.rect.centery = start_position[1]
        self.bounty = bounty

    @abc.abstractmethod
    def peel_layer(self):
        pass


class BalloonStateL1(BalloonState):
    """First, and lowest, level of BalloonState"""

    def peel_layer(self):
        """
        :return: None, represents no more layer beneath this layer
        In BalloonStateL1, the lowest balloon layer, indicate that there are no other layers to return
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return None  # there is no layer to return


class BalloonStateL2(BalloonState):
    def peel_layer(self):
        """
        :return: BalloonStateL1, the layer underneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon_state(BALLOON_L1, (self.rect.centerx, self.rect.centery))


class BalloonStateL3(BalloonState):
    def peel_layer(self):
        """
        :return: BalloonStateL2, the layer beneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon_state(BALLOON_L2, (self.rect.centerx, self.rect.centery))


class BalloonStateL4(BalloonState):
    def peel_layer(self):
        """
        :return: BalloonStateL3, the layer beneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon_state(BALLOON_L3, (self.rect.centerx, self.rect.centery))


class BalloonStateL5(BalloonState):
    def peel_layer(self):
        """
        :return: BalloonStateL2, the layer beneath this one
        The layer order is: 5 (highest), 4, 3, 2, 1(lowest)
        """
        return create_balloon_state(BALLOON_L4, (self.rect.centerx, self.rect.centery))


class Balloon(BalloonState):
    def __init__(self, current_balloon_state, balloon_path, path_index=0):
        """
        :param current_balloon_state: BalloonState, the current balloon to store in this context object
        :param balloon_path: path.Path, the path this balloon travels on
        :param path_index: int, the position of this balloon on its destined path
        This is the context object for a state machine. The states are the level of balloon, and transitions between states represents peeling layers off a balloon
        """

        assert isinstance(current_balloon_state, BalloonState), 'current_balloon_state must be a BalloonState type'

        pygame.sprite.Sprite.__init__(self)
        self.balloon_path = balloon_path
        self.path_index = path_index
        self.current_balloon_state = current_balloon_state

    def update(self, bullet_sprites):
        """
        :param bullet_sprites: pygame.sprite.Group, contains all the bullets in the game
        Update(...) is called every frame and checks if the current_balloon is hit by bullet or not
        """
        # logger.debug('inside Balloons update method')
        assert isinstance(bullet_sprites, pygame.sprite.Group), 'bullet_sprites must be a pygame.sprite.Group type'

        collided_bullets = pygame.sprite.spritecollide(self.current_balloon_state, bullet_sprites, False)
        if collided_bullets:
            # logger.info("inside collided_bullets loop")
            for collided_bullet in collided_bullets:
                #if the current balloon still exists (after handling a number of simultaneous collided_bullets
                if self.current_balloon_state is None:
                    return
                if isinstance(collided_bullet, bullet.StandardBullet):
                    collided_bullet.handle_collision_with_balloon()
                    self.peel_layer(collided_bullet.pop_power)  # represents should handle pop
                elif isinstance(collided_bullet, bullet.ExplosionBullet):
                    collided_bullet.handle_collision_with_balloon(
                        bullet_sprites)  # side note: explosion bullet will create more standard bullets
                    self.peel_layer(collided_bullet.pop_power)  # represents should handle pop
                elif isinstance(collided_bullet, bullet.TeleportationBullet):
                    collided_bullet.handle_collision_with_balloon()
                    self.move(-20)
                else:
                    raise NotImplementedError('the collided_bullet type is not allowed!')
        else:
            # logger.info("inside the collided_bullets else clause")
            self.move()

    def move(self, amount=1):
        """
        :param amount: int, the number of points to move forwards or backwards on the path. Positive is forwards; negative is backwards
        :return boolean, represents if the balloon has reached the end and thus, kills itself. Thus, the context can appropriately handle the case
        Increments the path_index so that the balloon progresses to the appropriate point on the path
        """
        assert 0 <= self.path_index < len(
            self.balloon_path), 'the path_index must be less than the length of the path points list'

        # logger.debug('inside the move method')

        # if the added amount is more than the path, then destroy this balloon
        # if it is less than the start index, place balloon at start
        # otherwise, the amount is within range of the path and place it there
        # logger.debug('value of path_index before if statement')
        if self.path_index + amount >= len(self.balloon_path):
            self.kill()
            life_point.decrease()
        elif self.path_index + amount < 0:
            # logger.debug('inside first elif')
            self.path_index = 0
        else:
            self.path_index += amount

        # logger.debug('the value of the path_index after if statementis: ' + str(self.path_index))
        # logger.debug('the x coordinate of the path is: ' + str(self.balloon_path[self.path_index][0]))
        # logger.debug('the y coordinate of the path is: ' + str(self.balloon_path[self.path_index][1]))

        self.current_balloon_state.rect.centerx = self.balloon_path[self.path_index][0]
        self.current_balloon_state.rect.centery = self.balloon_path[self.path_index][1]

    def peel_layer(self, number_of_layers=1):
        """
        :param number_of_layers: the number of layers to peel from the balloon state
        :return:
        """
        for _ in range(number_of_layers):
            # it's import to deposit here so that every deposit is made before the current ballon changes
            bank.deposit(self.current_balloon_state.bounty)
            self.current_balloon_state = self.current_balloon_state.peel_layer()
            if self.current_balloon_state is None:
                self.kill()
                break

    def get_centerX(self):
        """
        :return: the centerx of the current_balloon
        This is the equivalent of a getter
        """
        return self.current_balloon_state.rect.centerx

    def get_centerY(self):
        """
        :return: the centery of the current_balloon
         This si the equivalent for a getter
        """
        return self.current_balloon_state.rect.centery


def create_balloon_state(balloon_type, start_position):
    """
    :param balloon_type: str constant, which balloon to make (L1, L2, etc.)
    :param start_position: 2-element tuple, the start position of this balloon state
    :return: various BalloonLX
    Simple factory for returning new balloons and is particularly used by individual balloons to indicate the next balloon layer, for state changing
    """

    assert isinstance(balloon_type, str), 'balloon_type must be a string'
    assert isinstance(start_position, tuple) and len(start_position) == 2, 'path_to_move must a Path object'

    if balloon_type == BALLOON_L1:
        return BalloonStateL1(colour=colours.RED, dimension=(30, 30), start_position=start_position, bounty=10)
    elif balloon_type == BALLOON_L2:
        return BalloonStateL2(colour=colours.ORANGE, dimension=(30, 30), start_position=start_position, bounty=20)
    elif balloon_type == BALLOON_L3:
        return BalloonStateL3(colour=colours.YELLOW, dimension=(30, 30), start_position=start_position, bounty=30)
    elif balloon_type == BALLOON_L4:
        return BalloonStateL4(colour=colours.GREEN, dimension=(30, 30), start_position=start_position, bounty=40)
    elif balloon_type == BALLOON_L5:
        return BalloonStateL5(colour=colours.BLUE, dimension=(30, 30), start_position=start_position, bounty=50)

    raise NotImplementedError('Not implemented yet!')


def create_balloon(balloon_type, balloon_path, path_index=0):
    """
    :param balloon_type: str constant, which balloon will be the current starting balloon for this context
    :param balloon_path: the path the balloon moves on
    :param path_index: the starting index on the path to move on
    :return: Balloon, composing with a balloon
    Simple factory for creating the encapsulated balloon. Internally, composed of LX balloons
    """

    assert isinstance(balloon_type, str), 'balloon_type must be a string'
    assert isinstance(balloon_path, path.Path), 'balloon_path must be a balloon_path type'
    assert isinstance(path_index, int), 'path_index must be an integer'

    balloon_state = create_balloon_state(balloon_type=balloon_type,
                                         start_position=(balloon_path[path_index][0], balloon_path[path_index][1]))
    return Balloon(balloon_state, balloon_path, path_index)
