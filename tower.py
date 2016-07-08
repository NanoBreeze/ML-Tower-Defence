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

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')

LINEAR_TOWER = 'LINEAR_TOWER'
THREE_SIXTY_TOWER = 'THREE_SIXTY_TOWER'
EXPLOSION_TOWER = 'EXPLOSION_TOWER'
TELEPORTATION_TOWER = 'TELEPORTATION_TOWER'


class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""

    _attk_props = None #contains the attacking properties of this tower: speed, radius, pop power
    _attack_again_counter = None #used as a counter to increment when to attack, compared with AttackUpgrades.speed

    def __init__(self, colour, position, dimension, DISPLAYSURF):
        assert isinstance(colour, tuple), 'colour parameter must be a tuple instance'
        assert isinstance(position, tuple), 'position parameter must be a tuple instance'
        assert isinstance(dimension, tuple), 'dimension parameter must be a tuple instance'

        super().__init__()

        # self.attack_radius = attack_radius

        self.DISPLAYSURF = DISPLAYSURF
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        # pygame.draw.circle(DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius, 1)


    def update_speed(self):
        self._attk_props.upgrade_speed()

    def update_radius(self):
        self._attk_props.upgrade_radius()

    def update_pop_power(self):
        self._attk_props.update_pop_power()

    @abc.abstractmethod
    def update(self, ballon_sprites):
        pass

    @abc.abstractmethod
    def handle_is_clicked(self):
        pass


class LinearTower(Tower):
    """Attacks in a straight line"""

    def __init__(self, position, DISPLAYSURF):
        """

        :param position:
        :param DISPLAYSURF:
        """
        super().__init__(colour=colours.YELLOW, position=position, dimension=(50, 50), DISPLAYSURF=DISPLAYSURF)
        self._attk_props = AttackUpgrades((10, 20, 30), (80, 90, 100), (2, 3, 3)) #set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed #set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        """
        :param ballon_sprites: pygame.group.Group
        :param bullet_sprites: pygame.group.Group
        Hello there!
        """
        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius, 1)

        # possible to attack again
        if self._attack_again_counter == self._attk_props.speed:
            logger.info('INSIDE self.attack_again_counter_loop')
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                logger.info('INSIDE ballon_sprites for loop')
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    logger.info('INSIDE math.hypot if statement')
                    logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(ballon.get_centerX(), ballon.get_centerY()),
                                             pop_power=self._attk_props.pop_power))
                    self._attack_again_counter= 0
                    break
        else:
            self._attack_again_counter+= 1

    def handle_is_clicked(self, upgrade_icon_sprites):
        """
        :param upgrade_icon_sprites: pygame.sprite.Group
        :return: None, upgrade_icon_sprites is changed here
        Fills the upgrade_icon_sprite group with the upgrade icon sprites associated with this tower
        """
        assert isinstance(upgrade_icon_sprites, pygame.sprite.Group), 'upgrade_icon_sprites must be a pygame.sprite.Group() instance'
        logger.info('LinearTower is clicked')
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_SPEED_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_RADIUS_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_POP_POWER_ICON))

        return None


class ThreeSixtyTower(Tower):
    def __init__(self, position, DISPLAYSURF):
        super().__init__(colour=colours.CYAN, position=position, dimension=(40, 40), DISPLAYSURF=DISPLAYSURF)
        self._attk_props = AttackUpgrades((50, 20, 30), (180, 90, 100), (1, 2, 3)) #set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed #set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius, 1)

        # possible to attack again
        if self._attack_again_counter== self._attk_props.speed:
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx, self.rect.centery - 100),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx + 100, self.rect.centery - 100),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx + 100, self.rect.centery),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx + 100, self.rect.centery + 100),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx, self.rect.centery + 100),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx - 100, self.rect.centery + 100),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx - 100, self.rect.centery),
                                             pop_power=self._attk_props.pop_power),
                        bullet.create_bullet(bullet.STANDARD_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(self.rect.centerx - 100, self.rect.centery - 100),
                                             pop_power=self._attk_props.pop_power)
                    )
                    self._attack_again_counter = 0
                    break
        else:
            self._attack_again_counter+= 1

    def handle_is_clicked(self, upgrade_icon_sprites):
        """
        :param upgrade_icon_sprites: pygame.sprite.Group
        :return: None, upgrade_icon_sprites is changed here
        Fills the upgrade_icon_sprite group with the upgrade icon sprites associated with this tower
        """
        assert isinstance(upgrade_icon_sprites, pygame.sprite.Group), 'upgrade_icon_sprites must be a pygame.sprite.Group() instance'
        logger.info('ThreeSixtyTower is clicked')
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_SPEED_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_RADIUS_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_POP_POWER_ICON))

        return None


class ExplosionTower(Tower):
    """Shots ExplosionBullets"""

    def __init__(self, position, DISPLAYSURF):
        super().__init__(colour=colours.WHITE, position=position, dimension=(40, 40), DISPLAYSURF=DISPLAYSURF)
        self._attk_props = AttackUpgrades((5, 20, 30), (40, 90, 100), (1, 2, 3)) #set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed #set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):
        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius,
                           1)

        # possible to attack again
        if self._attack_again_counter== self._attk_props.speed:
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet.EXPLOSION_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(ballon.get_centerX(), ballon.get_centerY()),
                                             pop_power=self._attk_props.pop_power))
                    self._attack_again_counter= 0
                    break
        else:
            self._attack_again_counter+= 1

    def handle_is_clicked(self, upgrade_icon_sprites):
        """
        :param upgrade_icon_sprites: pygame.sprite.Group
        :return: None, upgrade_icon_sprites is changed here
        Fills the upgrade_icon_sprite group with the upgrade icon sprites associated with this tower
        """
        assert isinstance(upgrade_icon_sprites, pygame.sprite.Group), 'upgrade_icon_sprites must be a pygame.sprite.Group() instance'
        logger.info('ExplosionTower is clicked')
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_SPEED_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_RADIUS_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_POP_POWER_ICON))

        return None


class TeleportationTower(Tower):
    """Shoots TeleportationBullets"""

    def __init__(self, position, DISPLAYSURF):
        super().__init__(colour=colours.BROWN, position=position, dimension=(40, 40), DISPLAYSURF=DISPLAYSURF)
        self._attk_props = AttackUpgrades((10, 20, 30), (80, 90, 100), (1, 2, 3)) #set the upgrades appropriately
        self._attack_again_counter = self._attk_props.speed #set the counter to the 'shoot' position

    def update(self, ballon_sprites, bullet_sprites):

        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attk_props.radius,
                           1)

        # possible to attack again
        if self._attack_again_counter== self._attk_props.speed:
            # check if any ballons are within the range of the circle, which is currently set to 80
            for ballon in ballon_sprites:
                # if within range, print and create a bullet
                if math.hypot(ballon.get_centerX() - self.rect.centerx,
                              ballon.get_centerY() - self.rect.centery) <= self._attk_props.radius:
                    logger.debug('ATTACK! x is: {}. y is {}'.format(ballon.get_centerX(), ballon.get_centerY()))
                    bullet_sprites.add(
                        bullet.create_bullet(bullet.TELEPORTATION_BULLET, start=(self.rect.centerx, self.rect.centery),
                                             destination=(ballon.get_centerX(), ballon.get_centerY()),
                                             pop_power=self._attk_props.pop_power))
                    self._attack_again_counter= 0
                    break
        else:
            self._attack_again_counter+= 1

    def handle_is_clicked(self, upgrade_icon_sprites):
        """
        :param upgrade_icon_sprites: pygame.sprite.Group
        :return: None, upgrade_icon_sprites is changed here
        Fills the upgrade_icon_sprite group with the upgrade icon sprites associated with this tower
        """
        assert isinstance(upgrade_icon_sprites, pygame.sprite.Group), 'upgrade_icon_sprites must be a pygame.sprite.Group() instance'
        logger.info('TeleportationTower is clicked')
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_SPEED_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_RADIUS_ICON))
        upgrade_icon_sprites.add(icon.create_upgrade_icon(icon.UPGRADE_POP_POWER_ICON))

        return None


def create_tower(tower_type, position, DISPLAYSURF):
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

    def upgrade_speed(self):
        self.speed_index += 1
        assert self.speed_index <= len(self.speeds) -1, 'speed_index must be within the range of speeds list'
        self.speed = self.speeds[self.speed_index]

    def upgrade_radius(self):
        self.radius_index += 1
        assert self.radius_index <= len(self.radii) - 1, 'radius_index must be within the range of radii list'
        self.radius = self.radii[self.radius_index]

    def upgrade_pop_power(self):
        self.pop_power_index += 1
        assert self.pop_power_index <= len(self.pop_powers) - 1, 'pop_power_index must be within the range of pop_powers list'
        self.pop_power = self.pop_power[self.pop_power_index]
