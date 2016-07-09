import pygame
import logging
import logging.config
import abc

import tower
import colours
import sprite_groups
import bank

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

"""This module contains many icons used to create towers"""

LINEAR_TOWER_ICON = 'LINEAR_TOWER_ICON'
THREE_SIXTY_TOWER_ICON = 'THREE_SIXTY_TOWER_ICON'
EXPLOSION_TOWER_ICON = 'EXPLOSION_TOWER_ICON'
TELEPORTATION_TOWER_ICON = 'TELEPORTATION_TOWER_ICON'

UPGRADE_SPEED_ICON_1 = 'UPGRADE_SPEED_ICON_1'
UPGRADE_SPEED_ICON_2 = 'UPGRADE_SPEED_ICON_2'

UPGRADE_RADIUS_ICON_1 = 'UPGRADE_RADIUS_ICON_1'
UPGRADE_RADIUS_ICON_2 = 'UPGRADE_RADIUS_ICON_2'

UPGRADE_POP_POWER_ICON_1 = 'UPGRADE_POP_POWER_ICON_1'
UPGRADE_POP_POWER_ICON_2 = 'UPGRADE_POP_POWER_ICON_2'


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
    def on_left_mouse_button_up(self):
        pass

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

    def __init__(self, colour, position, dimension, tower_upgrade_method, upgrade_cost):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        :param upgrade_cost: the cost deducted from the bank to make this upgrade
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'
        assert isinstance(upgrade_cost, int), 'upgrade_cost must be an integer'

        self._tower_upgrade_method = tower_upgrade_method
        self._upgrade_cost = upgrade_cost

        super().__init__(colour, position, dimension)

    @abc.abstractmethod
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        pass

    def upgrade_and_replace_with_L2_upgrade_icon(self, upgrade_icon, upgrade_icon_sprites):
        next_upgrade_cost = self._tower_upgrade_method()
        upgrade_icon_sprites.add(create_upgrade_icon(upgrade_icon, self._tower_upgrade_method, next_upgrade_cost))
        self.kill()
        logger.info('all upgrade-icons in the sprite group are' + str(sprite_groups.upgrade_icon_sprites))

    def upgrade_and_replace_with_placeholder_upgrade_icon(self, upgrade_icon_sprites):
        self._tower_upgrade_method()
        upgrade_icon_sprites.add(create_placeholder_upgrade_icon(position=(self.rect.centerx, self.rect.centery),
                                                                 dimension=(self.image.get_width(), self.image.get_height())))

        self.kill()


class UpgradeSpeedBaseIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension, tower_upgrade_method, upgrade_cost):
        """
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param upgrade_cost: the cost deducted from the bank to make this upgrade
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'
        assert isinstance(upgrade_cost, int), 'upgrade_cost must be an integer'

        super().__init__(colour, position, dimension, tower_upgrade_method, upgrade_cost)


class UpgradeSpeedIcon1(UpgradeSpeedBaseIcon):
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        self.upgrade_and_replace_with_L2_upgrade_icon(UPGRADE_SPEED_ICON_2, upgrade_icon_sprites)
        bank.withdraw(self._upgrade_cost)


class UpgradeSpeedIcon2(UpgradeSpeedBaseIcon):
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        self.upgrade_and_replace_with_placeholder_upgrade_icon(upgrade_icon_sprites)
        bank.withdraw(self._upgrade_cost)


class UpgradeRadiusBaseIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension, tower_upgrade_method, upgrade_cost):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        :param dimension: 2-element tuple, the size of this icon
        :param upgrade_cost: the cost deducted from the bank to make this upgrade
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'
        assert isinstance(upgrade_cost, int), 'upgrade_cost must be an integer'

        super().__init__(colour, position, dimension, tower_upgrade_method, upgrade_cost)


class UpgradeRadiusIcon1(UpgradeRadiusBaseIcon):
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        self.upgrade_and_replace_with_L2_upgrade_icon(UPGRADE_RADIUS_ICON_2, upgrade_icon_sprites)
        bank.withdraw(self._upgrade_cost)


class UpgradeRadiusIcon2(UpgradeRadiusBaseIcon):
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        self.upgrade_and_replace_with_placeholder_upgrade_icon(upgrade_icon_sprites)
        bank.withdraw(self._upgrade_cost)


class UpgradePopPowerBaseIcon(UpgradeIcon):
    def __init__(self, colour, position, dimension, tower_upgrade_method, upgrade_cost):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param tower_upgrade_method: method of the related upgrade method from the associated tower
        :param upgrade_cost: the cost deducted from the bank to make this upgrade
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'
        assert isinstance(upgrade_cost, int), 'upgrade_cost must be an integer'

        super().__init__(colour, position, dimension, tower_upgrade_method, upgrade_cost)


class UpgradePopPowerIcon1(UpgradePopPowerBaseIcon):
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        self.upgrade_and_replace_with_L2_upgrade_icon(UPGRADE_POP_POWER_ICON_2, upgrade_icon_sprites)
        bank.withdraw(self._upgrade_cost)


class UpgradePopPowerIcon2(UpgradePopPowerBaseIcon):
    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        self.upgrade_and_replace_with_placeholder_upgrade_icon(upgrade_icon_sprites)
        bank.withdraw(self._upgrade_cost)


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

        super().__init__(colour, position, dimension, lambda: print('dummy function from placeholder icon. This function should never be called beause placeholder icon is the equivalent of a Null object'), 0)

    def on_left_mouse_button_up(self, upgrade_icon_sprites):
        pass

class SellTowerIcon(Icon):
    def __init__(self, colour, position, dimension, kill_tower_method):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param kill_tower_method: the tower that will be solve if this button is clicked
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert hasattr(kill_tower_method, '__call__'), 'kill_tower_method must be a callable (eg, method)'

        self.kill_tower_method = kill_tower_method

        super().__init__(colour, position, dimension)

    def on_left_mouse_button_up(self):
        tower_sell_price = self.kill_tower_method()
        bank.deposit(tower_sell_price)


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


def create_upgrade_icon(upgrade_icon_type, tower_upgrade_method, upgrade_cost):
    """
    :param upgrade_icon_type: str constant, specifies which upgrade icon to make
    :param tower_upgrade_method: function, the tower this upgrade icon is associated. Click on this upgrade icon will cause the specified tower to be upgraded
    :param upgrade_cost: the amount to withdraw from bank balance to make this upgrade
    :return: Upgrade...Icon, eg, UpgradeSpeedBaseIcon
    A simple factory that returns a specified upgrade icon associated with a given tower
    """

    assert isinstance(upgrade_icon_type, str), 'tower_icon_type must be a string type'
    assert hasattr(tower_upgrade_method, '__call__'), '_tower_upgrade_method must be a callable (eg, method)'

    if upgrade_icon_type == UPGRADE_SPEED_ICON_1:
        return UpgradeSpeedIcon1(colour=colours.WHITE,
                                 position=(100, 350),
                                 dimension=(50, 50),
                                 tower_upgrade_method=tower_upgrade_method,
                                 upgrade_cost=upgrade_cost)

    elif upgrade_icon_type == UPGRADE_SPEED_ICON_2:
        return UpgradeSpeedIcon2(colour=colours.BLACK,
                                 position=(100, 350),
                                 dimension=(50, 50),
                                 tower_upgrade_method=tower_upgrade_method,
                                 upgrade_cost=upgrade_cost)

    elif upgrade_icon_type == UPGRADE_RADIUS_ICON_1:
        return UpgradeRadiusIcon1(colour=colours.WHITE,
                                  position=(200, 350),
                                  dimension=(50, 50),
                                  tower_upgrade_method=tower_upgrade_method,
                                  upgrade_cost=upgrade_cost)

    elif upgrade_icon_type == UPGRADE_RADIUS_ICON_2:
        return UpgradeRadiusIcon2(colour=colours.BLACK,
                                  position=(200, 350),
                                  dimension=(50, 50),
                                  tower_upgrade_method=tower_upgrade_method,
                                  upgrade_cost=upgrade_cost)

    elif upgrade_icon_type == UPGRADE_POP_POWER_ICON_1:
        return UpgradePopPowerIcon1(colour=colours.WHITE,
                                    position=(300, 350),
                                    dimension=(50, 50),
                                    tower_upgrade_method=tower_upgrade_method,
                                    upgrade_cost=upgrade_cost)

    elif upgrade_icon_type == UPGRADE_POP_POWER_ICON_2:
        return UpgradePopPowerIcon2(colour=colours.BLACK,
                                    position=(300, 350),
                                    dimension=(50, 50),
                                    tower_upgrade_method=tower_upgrade_method,
                                    upgrade_cost=upgrade_cost)

    raise NotImplementedError('the specified upgrade icon is not implemented')


def create_placeholder_upgrade_icon(position, dimension):
    """Create a placeholder icon. Equivalent to a null object"""
    return UpgradeIconPlaceholder(colour=colours.BROWN,
                                  position=position,
                                  dimension=dimension)

def create_sell_tower_icon(kill_tower_method):
    return SellTowerIcon(colour=colours.ORANGE, position=(50, 375), dimension=(40, 20), kill_tower_method=kill_tower_method)
