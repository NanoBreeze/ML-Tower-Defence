import pygame
import logging
import logging.config
import abc
import tower

import colours

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

"""This module contains many icons used to create towers"""

LINEAR_TOWER_ICON = 'LINEAR_TOWER_ICON'
THREE_SIXTY_TOWER_ICON = 'THREE_SIXTY_TOWER_ICON'
EXPLOSION_TOWER_ICON = 'EXPLOSION_TOWER_ICON'
TELEPORTATION_TOWER_ICON = 'TELEPORTATION_TOWER_ICON'

UPGRADE_SPEED_ICON = 'UPGRADE_SPEED_ICON'
UPGRADE_RADIUS_ICON = 'UPGRADE_RADIUS_ICON'
UPGRADE_POP_POWER_ICON = 'UPGRADE_POP_POWER_ICON'


class Icon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    def __init__(self, colour, position, dimension):
        super().__init__()
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def update(self, mouse_position):
        """Move the icon to the position of the mouse"""
        self.rect.centerx = mouse_position[0]
        self.rect.centery = mouse_position[1]

    @abc.abstractmethod
    def on_left_mouse_button_up(self):
        """Handles event where the user clicked on this icon"""
        pass


class TowerIcon(Icon, metaclass=abc.ABCMeta):
    _tower_type = None

    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)

    @abc.abstractmethod
    #  reason for this copy method is because Python throws an error after deep copying aomething that contains a Surface object
    # thus, each icon has its own copy method that returns a NEW icon
    def duplicate(self):
        pass


class LinearTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)
        self._tower_type = tower.LINEAR_TOWER

    def on_left_mouse_button_up(self):
        logger.info('The LinearTowerIcon is pressed')
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        return create_tower_icon(LINEAR_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class ThreeSixtyTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)
        self._tower_type = tower.THREE_SIXTY_TOWER

    def on_left_mouse_button_up(self):
        logger.info('The ThreeSixtyTowerIcon is pressed')
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        return create_tower_icon(THREE_SIXTY_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class ExplosionTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)
        self._tower_type = tower.EXPLOSION_TOWER

    def on_left_mouse_button_up(self):
        logger.info('The ExplosionTowerIcon is pressed')
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        return create_tower_icon(EXPLOSION_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class TeleportationTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)
        self._tower_type = tower.TELEPORTATION_TOWER

    def on_left_mouse_button_up(self):
        logger.info('The TeleportationTowerIcon is pressed')
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        return create_tower_icon(TELEPORTATION_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class UpgradeIcon(Icon, metaclass=abc.ABCMeta):
    """
    Base class for Upgrade Icons, derived classes include upgrading spee, radius and pop power
    """

    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)


class UpgradeSpeedIcon(UpgradeIcon):
    """
    Icon for upgrading tower's speed, contains icon position, dimension, and colour
    """

    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        logger.info('The UpgradSpeedIcon is pressed')


class UpgradeRadiusIcon(UpgradeIcon):
    """
    Icon for upgrading tower's radius, contains icon position, dimension, and colour
    """

    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        logger.info('The UpgradeRadiusIcon is pressed')


class UpgradePopPowerIcon(UpgradeIcon):
    """
    Icon for upgrading tower's pop power, contains icon position, dimension, and colour
    """

    def __init__(self, colour, position, dimension):
        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        logger.info('The UpgradePopPowerIcon is pressed')


def create_tower_icon(icon_type, position):
    if icon_type == LINEAR_TOWER_ICON:
        return LinearTowerIcon(colour=colours.YELLOW,
                               position=position,
                               dimension=(50, 50))
    elif icon_type == THREE_SIXTY_TOWER_ICON:
        return ThreeSixtyTowerIcon(colour=colours.CYAN,
                                   position=position,
                                   dimension=(40, 40))
    elif icon_type == EXPLOSION_TOWER_ICON:
        return ExplosionTowerIcon(colour=colours.WHITE,
                                  position=position,
                                  dimension=(40, 40))
    elif icon_type == TELEPORTATION_TOWER_ICON:
        return TeleportationTowerIcon(colour=colours.BROWN,
                                      position=position,
                                      dimension=(40, 40))

    raise NotImplementedError('the specified tower icon_type is not implemented')


def create_upgrade_icon(icon_type):
    if icon_type == UPGRADE_SPEED_ICON:
        return UpgradeSpeedIcon(colour=colours.WHITE, position=(100, 350), dimension=(50, 50))
    elif icon_type == UPGRADE_RADIUS_ICON:
        return UpgradeRadiusIcon(colour=colours.WHITE, position=(200, 350), dimension=(50, 50))
    elif icon_type == UPGRADE_POP_POWER_ICON:
        return UpgradePopPowerIcon(colour=colours.WHITE, position=(300, 350), dimension=(50, 50))

    raise NotImplementedError('the specified upgrade icon is not implemented')
