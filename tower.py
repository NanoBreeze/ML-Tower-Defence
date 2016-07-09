import abc
import pygame
import pygame.surface
import pygame.sprite
import math
import bullet
import colours
import logging
import icon
import logging.config
import sprite_groups

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')

LINEAR_TOWER = 'LINEAR_TOWER'
THREE_SIXTY_TOWER = 'THREE_SIXTY_TOWER'
EXPLOSION_TOWER = 'EXPLOSION_TOWER'
TELEPORTATION_TOWER = 'TELEPORTATION_TOWER'


class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""

    _attk_props = None  # contains the attacking properties of this tower: speed, radius, pop power
    _attack_again_counter = None  # used as a counter to increment when to attack, compared with AttackUpgrades.speed

    def __init__(self, colour, position, dimension, cost, DISPLAYSURF):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param cost: int, the amount of money to withdraw from balance to create this tower
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert isinstance(cost, int), 'cost must be an integer'
        assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame Surface object'

        super().__init__()

        self.DISPLAYSURF = DISPLAYSURF
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.cost = cost

    def upgrade_speed(self):
        self._attk_props.upgrade_speed()

    def upgrade_radius(self):
        self._attk_props.upgrade_radius()

    def upgrade_pop_power(self):
        self._attk_props.upgrade_pop_power()

    @abc.abstractmethod
    def update(self, ballon_sprites):
        pass

    def handle_is_clicked(self, upgrade_icon_sprites):
        """
        :param upgrade_icon_sprites: pygame.sprite.Group, contains all three upgrade icons in the game
        :return: None, upgrade_icon_sprites is changed here to include the three upgrade sprite
        Fills the upgrade_icon_sprite group with the upgrade icon sprites associated with this tower. If upgrade is already at max, show nothing
        """
        assert isinstance(upgrade_icon_sprites, pygame.sprite.Group), 'upgrade_icon_sprites must be a pygame.sprite.Group() instance'


        logger.info('inside handle_is_clicked. About to call next speed index')
        next_speed_upgrade_index = self._attk_props.get_next_speed_index_for_upgrade()
        logger.info('after call for next speed index. Its value is ' + str(next_speed_upgrade_index))
        logger.info('inside handle_is_clicked. About to call next radius index')
        next_radius_upgrade_index = self._attk_props.get_next_radius_index_for_upgrade()
        logger.info('after call for next radius index. Its value is ' + str(next_radius_upgrade_index))
        next_pop_power_upgrade_index = self._attk_props.get_next_pop_power_index_for_upgrade()

        if next_speed_upgrade_index == 1:
            upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_SPEED_ICON_1, self.upgrade_speed))
        elif next_speed_upgrade_index == 2:
            upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_SPEED_ICON_2, self.upgrade_speed))
        elif next_speed_upgrade_index is None:  # make a placeholder (equivalent to null object)
            upgrade_icon_sprites.add(icon.create_placeholder_upgrade_icon(position=(100, 350), dimension=(50, 50)))

        if next_radius_upgrade_index == 1:
            upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_RADIUS_ICON_1, self.upgrade_radius))
        elif next_radius_upgrade_index == 2:
            upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_RADIUS_ICON_2, self.upgrade_radius))
        elif next_radius_upgrade_index is None:  # make a placeholder (equivalent to null object)
            upgrade_icon_sprites.add(icon.create_placeholder_upgrade_icon(position=(200, 350), dimension=(50, 50)))

        if next_pop_power_upgrade_index == 1:
            upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_POP_POWER_ICON_1, self.upgrade_pop_power))
        elif next_pop_power_upgrade_index == 2:
            upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_POP_POWER_ICON_2, self.upgrade_pop_power))
        elif next_pop_power_upgrade_index is None:  # make a placeholder (equivalent to null object)
            upgrade_icon_sprites.add(icon.create_placeholder_upgrade_icon(position=(300, 350), dimension=(50, 50)))

        return None


class LinearTower(Tower):
    """Attacks in a straight line"""

    def __init__(self, position, DISPLAYSURF):
        """
        :param position: 2-element tuple, where this icon is to be placed
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        Creates a LinearTower (shoots LinearBullets)
        """

        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame Surface object'

        super().__init__(colour=colours.YELLOW,
                         position=position,
                         dimension=(50, 50),
                         cost=10,
                         DISPLAYSURF=DISPLAYSURF)

        self._attk_props = AttackUpgrades((10, 20, 30), (80, 90, 100), (1, 2, 3))  # set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed  # set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        """
        :param ballon_sprites: pygame.group.Group
        :param bullet_sprites: pygame.group.Group
        Checks if there are any balloons in the vicinity and if so, attack a bullet at it
        """

        assert isinstance(ballon_sprites, sprite_groups.BallonGroup), "ballon_sprites must be a pygame.sprite.Group object"
        assert isinstance(bullet_sprites, pygame.sprite.Group), "bullet_sprites must be a pygame.sprite.Group object"

        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius, 1)

        # checks if it's possible to attack again
        if self._attack_again_counter == self._attk_props.speed:
            # logger.info('INSIDE self.attack_again_counter_loop')
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # logger.info('INSIDE ballon_sprites for loop')
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    # logger.info('INSIDE math.hypot if statement')
                    bullet_sprites.add(
                        bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(ballon.get_centerX(), ballon.get_centerY()),
                                             pop_power=self._attk_props.pop_power))
                    self._attack_again_counter = 0
                    break
        else:
            self._attack_again_counter += 1


class ThreeSixtyTower(Tower):
    def __init__(self, position, DISPLAYSURF):
        """
        :param position: 2-element tuple, where this icon is to be placed
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        Creates a ThreeSixtyTower (shoots 8 StandardBullets)
        """

        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame Surface object'

        super().__init__(colour=colours.CYAN,
                         position=position,
                         dimension=(40, 40),
                         cost=20,
                         DISPLAYSURF=DISPLAYSURF)

        self._attk_props = AttackUpgrades((50, 20, 30), (180, 90, 100), (1, 2, 3))  # set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed  # set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        """
        :param ballon_sprites: pygame.group.Group
        :param bullet_sprites: pygame.group.Group
        Checks if there are any balloons in the vicinity and if so, attack a bullet at it
        """

        assert isinstance(ballon_sprites, sprite_groups.BallonGroup), "ballon_sprites must be a pygame.sprite.Group object"
        assert isinstance(bullet_sprites, pygame.sprite.Group), "bullet_sprites must be a pygame.sprite.Group object"

        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius, 1)

        # checks if it is possible to attack again
        if self._attack_again_counter == self._attk_props.speed:
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    # logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx, self.rect.centery - 100),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx + 100, self.rect.centery - 100),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx + 100, self.rect.centery),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx + 100, self.rect.centery + 100),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx, self.rect.centery + 100),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx - 100, self.rect.centery + 100),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx - 100, self.rect.centery),
                                             pop_power=self._attk_props.pop_power),

                        bullet.create_bullet(bullet.STANDARD_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx - 100, self.rect.centery - 100),
                                             pop_power=self._attk_props.pop_power)
                    )
                    self._attack_again_counter = 0
                    break
        else:
            self._attack_again_counter += 1


class ExplosionTower(Tower):
    """Shoots ExplosionBullets"""

    def __init__(self, position, DISPLAYSURF):
        """
        :param position: 2-element tuple, where this icon is to be placed
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        Creates an ExplosionTower (shoots ExplosionBullets)
        """

        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame Surface object'

        super().__init__(colour=colours.WHITE,
                         position=position,
                         dimension=(40, 40),
                         cost=30,
                         DISPLAYSURF=DISPLAYSURF)

        self._attk_props = AttackUpgrades((5, 20, 30), (40, 90, 100), (1, 2, 3))  # set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed  # set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        """
        :param ballon_sprites: pygame.group.Group
        :param bullet_sprites: pygame.group.Group
        Checks if there are any balloons in the vicinity and if so, attack a bullet at it
        """

        assert isinstance(ballon_sprites, sprite_groups.BallonGroup), "ballon_sprites must be a pygame.sprite.Group object"
        assert isinstance(bullet_sprites, pygame.sprite.Group), "bullet_sprites must be a pygame.sprite.Group object"

        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius, 1)

        # checks if it is possible to attack again
        if self._attack_again_counter == self._attk_props.speed:
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    #logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet_type=bullet.EXPLOSION_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(ballon.get_centerX(), ballon.get_centerY()),
                                             pop_power=self._attk_props.pop_power))
                    self._attack_again_counter = 0
                    break
        else:
            self._attack_again_counter += 1


class TeleportationTower(Tower):
    """Shoots TeleportationBullets"""

    def __init__(self, position, DISPLAYSURF):
        """
        :param position: 2-element tuple, where this icon is to be placed
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        Creates a TeleportationTower (shoots TeleportationBullets)
        """

        super().__init__(colour=colours.BROWN,
                         position=position,
                         dimension=(40, 40),
                         cost=40,
                         DISPLAYSURF=DISPLAYSURF)

        self._attk_props = AttackUpgrades((10, 20, 30), (80, 90, 100), (1, 2, 3))  # set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed  # set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        """
        :param ballon_sprites: pygame.group.Group
        :param bullet_sprites: pygame.group.Group
        Checks if there are any balloons in the vicinity and if so, attack a bullet at it
        """

        assert isinstance(ballon_sprites, sprite_groups.BallonGroup), "ballon_sprites must be a pygame.sprite.Group object"
        assert isinstance(bullet_sprites, pygame.sprite.Group), "bullet_sprites must be a pygame.sprite.Group object"

        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius,
                           1)

        # checks if it possible to attack again
        if self._attack_again_counter == self._attk_props.speed:
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    #logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet_type=bullet.TELEPORTATION_BULLET,
                                             start=(self.rect.centerx, self.rect.centery),
                                             destination=(ballon.get_centerX(), ballon.get_centerY()),
                                             pop_power=self._attk_props.pop_power))
                    self._attack_again_counter = 0
                    break
        else:
            self._attack_again_counter += 1


def create_tower(tower_type, position, DISPLAYSURF):
    """
    :param tower_type: str constant, which tower to create
    :param position: 2-element tuple, where the tower is to be created
    :param DISPLAYSURF: pygame.Surface, the main Surface object
    :return: XTower, eg, LinearTower
    A simple factory for creating towers
    """

    assert isinstance(tower_type, str), 'tower_icon_type must be a string type'
    assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
    assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame.Surface object'

    if tower_type == LINEAR_TOWER:
        return LinearTower(position, DISPLAYSURF)
    elif tower_type == THREE_SIXTY_TOWER:
        return ThreeSixtyTower(position, DISPLAYSURF)
    elif tower_type == EXPLOSION_TOWER:
        return ExplosionTower(position, DISPLAYSURF)
    elif tower_type == TELEPORTATION_TOWER:
        return TeleportationTower(position, DISPLAYSURF)

    raise NotImplementedError('The passed in tower_type is not implemented')


class AttackUpgrades:
    """upgrades include speed, radius, and pop_power"""

    def __init__(self, upgrade_speeds, upgrade_radii, upgrade_pop_powers):
        """
        :param upgrade_speeds: a tuple containing the order that speed upgrades happen
        :param upgrade_radii: a tuple containing the order that radius upgrades happen
        :param upgrade_pop_powers: a tuple containing the order that pop power upgrades happen
        Sets the possible upgrade values and set the current attack properties to the first element of each
        """
        assert isinstance(upgrade_speeds, tuple), 'upgrade_speed must be a list'
        assert isinstance(upgrade_radii, tuple), 'upgrade_radii must be a list'
        assert isinstance(upgrade_pop_powers, tuple), 'upgrade_pop_powers must be a list'

        self.speeds = upgrade_speeds
        self.radii = upgrade_radii
        self.pop_powers = upgrade_pop_powers

        self.speed_index = 0
        self.radius_index = 0
        self.pop_power_index = 0

        self.speed = upgrade_speeds[self.speed_index]
        self.radius = upgrade_radii[self.radius_index]
        self.pop_power = upgrade_pop_powers[self.pop_power_index]

    def get_next_speed_index_for_upgrade(self):
        """
        :return: int or None, self.speed_index + 1, get the index of the next speed (to upgrade to) from the speeds tuple
        """
        logger.info('speed_index before incrementing' + str(self.speed_index))
        next_speed_index = self.speed_index + 1
        logger.info('speed_index after incrementing: ' + str(next_speed_index))
        if next_speed_index < len(self.speeds):  # make sure that the next speed index isn't out of bounds
            logger.info('inside if, returning next_speed_index')
            return next_speed_index
        else:
            logger.info('inside else, returning None')
            return None

    def upgrade_speed(self):
        logger.info('upgrade_speed before incrementing')
        self.speed_index += 1
        logger.info('upgrade_speed after incrementing: ' + str(self.speed_index))
        assert self.speed_index < len(self.speeds), 'speed_index must be within the range of speeds list'
        self.speed = self.speeds[self.speed_index]

    def get_next_radius_index_for_upgrade(self):
        """
        :return: int or None, self.speed_index + 1, get the index of the next speed (to upgrade to) from the speeds tuple
        """
        logger.info('radius_index before incrementing: ' + str(self.radius_index))
        next_radius_index = self.radius_index + 1
        logger.info('radius index after incrementing: ' + str(next_radius_index))

        if next_radius_index < len(self.radii):  # make sure that the next radius index isn't out of bounds
            logger.info('inside if, returning next_radius_index')
            return next_radius_index
        else:
            logger.info('inside else, returning None')
            return None

    def upgrade_radius(self):
        logger.info('upgrade_radius before incrementing')
        self.radius_index += 1
        logger.info('upgrade_radius after incrementing: ' + str(self.radius_index))

        assert self.radius_index < len(self.radii), 'radius_index must be within the range of radii list'
        self.radius = self.radii[self.radius_index]

    def get_next_pop_power_index_for_upgrade(self):
        """
        :return: int or None, get the index of the next speed (to upgrade to) from the speeds tuple
        """
        logger.info('pop_power_index before incrementing: ' + str(self.pop_power_index))
        next_pop_power_index = self.pop_power_index + 1
        logger.info('pop_power_index after incrementing: ' + str(next_pop_power_index))
        if next_pop_power_index < len(self.pop_powers):  # make sure that the next pop power index isn't out of bounds
            logger.info('inside if, returning next_pop_power_index')
            return next_pop_power_index
        else:
            logger.info('inside else, returning None')
            return None

    def upgrade_pop_power(self):
        logger.info('upgrade_pop_power before incrementing')
        self.pop_power_index += 1
        logger.info('upgrade_pop_power after incrementing: ' + str(self.pop_power_index))
        assert self.pop_power_index < len(self.pop_powers), 'pop_power_index must be within the range of pop_powers list'
        self.pop_power = self.pop_powers[self.pop_power_index]
