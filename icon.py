import pygame
import logging.config
import abc

import tower
import colours

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

LINEAR_TOWER_ICON = 'LINEAR_TOWER_ICON'
THREE_SIXTY_TOWER_ICON = 'THREE_SIXTY_TOWER_ICON'
EXPLOSION_TOWER_ICON = 'EXPLOSION_TOWER_ICON'
TELEPORTATION_TOWER_ICON = 'TELEPORTATION_TOWER_ICON'

UPGRADE_SPEED_ICONS = 'UPGRADE_SPEED_ICONS'
UPGRADE_RADIUS_ICONS = 'UPGRADE_RADIUS_ICONS'
UPGRADE_POP_POWER_ICONS = 'UPGRADE_POP_POWER_ICONS'


class Icon(pygame.sprite.Sprite):
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
    def on_click(self, upgrade_icon_sprites):
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

    def on_click(self):
        """
        :return: a duplicate of this icon (not same reference)
         Change colour of icon and return a duplicate of this icon
        """
        self.image.fill(colours.ORANGE)
        return self.duplicate()

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

    def __init__(self, colour, position, dimension, tower_upgrade_method):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'

        self._tower_upgrade_method = tower_upgrade_method
        super().__init__(colour, position, dimension)

    def on_click(self, upgrade_icon_sprites):
        self._tower_upgrade_method()


class UpgradeSpeedBaseIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension, tower_upgrade_method):
        """
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'

        super().__init__(colour, position, dimension, tower_upgrade_method)


class UpgradeSpeedIcon1(UpgradeSpeedBaseIcon):
    pass


class UpgradeSpeedIcon2(UpgradeSpeedBaseIcon):
    pass


class UpgradeRadiusBaseIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension, tower_upgrade_method):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'

        super().__init__(colour, position, dimension, tower_upgrade_method)


class UpgradeRadiusIcon1(UpgradeRadiusBaseIcon):
    pass


class UpgradeRadiusIcon2(UpgradeRadiusBaseIcon):
    pass


class UpgradePopPowerBaseIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension, tower_upgrade_method):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'

        super().__init__(colour, position, dimension, tower_upgrade_method)


class UpgradePopPowerIcon1(UpgradePopPowerBaseIcon):
    pass


class UpgradePopPowerIcon2(UpgradePopPowerBaseIcon):
    pass


class UpgradeIconPlaceholder(UpgradeIcon):
    """Indicates that the specified is upgrade is already at max. This is the equivalent of a None object"""

    def __init__(self, colour, position, dimension):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'

        super().__init__(colour, position, dimension, lambda: print(
            'dummy function from placeholder icon. This function should never be called beause placeholder icon is the equivalent of a Null object'))


class SellTowerIcon(Icon):
    def __init__(self, colour, position, dimension, sell_tower_method):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param sell_tower_method: the tower that will be solve if this button is clicked
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(sell_tower_method, '__call__'), 'sell_tower_method must be a callable (eg, method)'

        self.sell_tower_method = sell_tower_method

        super().__init__(colour, position, dimension)

    def on_click(self):
        self.sell_tower_method()


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


def create_upgrade_type_icons_batch(icon_type, tower_upgrade_method):
    """
    :param icon_type, str constant, the type of icons to make, eg, speed
    :param tower_upgrade_method: function, the method to call when this icon is clicked
    :return: tuple of icons, (S1, S2, P)
    Creates all the tower upgrade icons by group, eg, speed, and they contain the method to call
    """

    assert hasattr(tower_upgrade_method, '__call__'), 'tower_upgrade_method must be a method type'

    if icon_type == UPGRADE_SPEED_ICONS:
        return (
            UpgradeSpeedIcon1(colour=colours.WHITE,
                              position=(100, 350),
                              dimension=(50, 50),
                              tower_upgrade_method=tower_upgrade_method),
            UpgradeSpeedIcon2(colour=colours.BLACK,
                              position=(100, 350),
                              dimension=(50, 50),
                              tower_upgrade_method=tower_upgrade_method)
        )
    elif icon_type == UPGRADE_RADIUS_ICONS:
        return (
            UpgradeRadiusIcon1(colour=colours.WHITE,
                               position=(200, 350),
                               dimension=(50, 50),
                               tower_upgrade_method=tower_upgrade_method),
            UpgradeRadiusIcon2(colour=colours.BLACK,
                               position=(200, 350),
                               dimension=(50, 50),
                               tower_upgrade_method=tower_upgrade_method)
        )
    elif icon_type == UPGRADE_POP_POWER_ICONS:
        return (
            UpgradePopPowerIcon1(colour=colours.WHITE,
                                 position=(300, 350),
                                 dimension=(50, 50),
                                 tower_upgrade_method=tower_upgrade_method),
            UpgradePopPowerIcon2(colour=colours.BLACK,
                                 position=(300, 350),
                                 dimension=(50, 50),
                                 tower_upgrade_method=tower_upgrade_method)
        )
    raise NotImplementedError('The specified icon_type, {0}, is not implemented'.format(icon_type))


def create_placeholder_upgrade_icon(position, dimension):
    """Create a placeholder icon. Equivalent to a null object"""
    return UpgradeIconPlaceholder(colour=colours.BROWN,
                                  position=position,
                                  dimension=dimension)


def create_sell_tower_icon(sell_tower_method):
    return SellTowerIcon(colour=colours.ORANGE, position=(50, 375), dimension=(40, 20), sell_tower_method=sell_tower_method)
