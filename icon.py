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
    """The base class for all icons"""

    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__()
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def update(self, mouse_position):
        """
        :param mouse_position: 2-element tuple, the x and y coordinates of the mouse
        Called every frame, sets the centerx and centery positions of this icon
        """
        self.rect.centerx = mouse_position[0]
        self.rect.centery = mouse_position[1]

    @abc.abstractmethod
    def on_left_mouse_button_up(self):
        """Handles event where the user clicked on this icon"""
        pass


class TowerIcon(Icon, metaclass=abc.ABCMeta):
    """Base class for all Tower-related icons"""

    _tower_type = None

    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)

    @abc.abstractmethod
    #  reason for this copy method is because Python throws an error after deep copying aomething that contains a Surface object
    # thus, each icon has its own copy method that returns a NEW icon
    def duplicate(self):
        pass


class LinearTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)
        self._tower_type = tower.LINEAR_TOWER

    def on_left_mouse_button_up(self):
        """Change this icon's colour when it is clicked"""
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        """
        :return: LinearTowerIcon
        Create a duplicate icon of this one
        """
        return create_tower_icon(LINEAR_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class ThreeSixtyTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)
        self._tower_type = tower.THREE_SIXTY_TOWER

    def on_left_mouse_button_up(self):
        """Change this icon's colour when it is clicked"""
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        """
        :return: ThreeSixtyTowerIcon
        Create a duplicate icon of this one
        """
        return create_tower_icon(THREE_SIXTY_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class ExplosionTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)
        self._tower_type = tower.EXPLOSION_TOWER

    def on_left_mouse_button_up(self):
        """Change this icon's colour when it is clicked"""
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        """
        :return: ThreeSixtyTowerIcon
        Create a duplicate icon of this one
        """
        return create_tower_icon(EXPLOSION_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class TeleportationTowerIcon(TowerIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)
        self._tower_type = tower.TELEPORTATION_TOWER

    def on_left_mouse_button_up(self):
        """Change this icon's colour when it is clicked"""
        self.image.fill(colours.ORANGE)

    def duplicate(self):
        """
        :return: TeleportationTowerIcon
        Create a duplicate icon of this one
        """
        return create_tower_icon(TELEPORTATION_TOWER_ICON, (self.rect.centerx, self.rect.centery))


class UpgradeIcon(Icon, metaclass=abc.ABCMeta):
    """
    Base class for all Upgrade-relatedIcons
    """

    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)


class UpgradeSpeedIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        logger.info('The UpgradSpeedIcon is pressed')


class UpgradeRadiusIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        logger.info('The UpgradeRadiusIcon is pressed')


class UpgradePopPowerIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        logger.info('The UpgradePopPowerIcon is pressed')


def create_tower_icon(tower_icon_type, position):
    """
    :param tower_icon_type: str constant, specifies which  tower icon to make
    :param position: 2-element tuple, the starting position of the icon
    :return: ...TowerIcon, eg, LinearTowerIcon
    A simple factory that returns a specified tower icon
    """

    assert isinstance(tower_icon_type, str), 'tower_icon_type must be a string type'
    assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'

    if tower_icon_type == LINEAR_TOWER_ICON:
        return LinearTowerIcon(colour=colours.YELLOW,
                               position=position,
                               dimension=(50, 50))

    elif tower_icon_type == THREE_SIXTY_TOWER_ICON:
        return ThreeSixtyTowerIcon(colour=colours.CYAN,
                                   position=position,
                                   dimension=(40, 40))

    elif tower_icon_type == EXPLOSION_TOWER_ICON:
        return ExplosionTowerIcon(colour=colours.WHITE,
                                  position=position,
                                  dimension=(40, 40))

    elif tower_icon_type == TELEPORTATION_TOWER_ICON:
        return TeleportationTowerIcon(colour=colours.BROWN,
                                      position=position,
                                      dimension=(40, 40))

    raise NotImplementedError('the specified tower tower_icon_type is not implemented')


def create_upgrade_icon(upgrade_icon_type):
    """
    :param upgrade_icon_type: str constant, specifies which upgrade icon to make
    :return: Upgrade...Icon, eg, UpgradeSpeedIcon
    A simple factory that returns a specified upgrade icon
    """

    assert isinstance(upgrade_icon_type, str), 'tower_icon_type must be a string type'

    if upgrade_icon_type == UPGRADE_SPEED_ICON:
        return UpgradeSpeedIcon(colour=colours.WHITE,
                                position=(100, 350),
                                dimension=(50, 50))

    elif upgrade_icon_type == UPGRADE_RADIUS_ICON:
        return UpgradeRadiusIcon(colour=colours.WHITE,
                                 position=(200, 350),
                                 dimension=(50, 50))

    elif upgrade_icon_type == UPGRADE_POP_POWER_ICON:
        return UpgradePopPowerIcon(colour=colours.WHITE,
                                   position=(300, 350),
                                   dimension=(50, 50))

    raise NotImplementedError('the specified upgrade icon is not implemented')
