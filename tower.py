import abc
import pygame
import pygame.surface
import pygame.sprite
import math
import bullet
import colours
import icon
import logging.config
import sprite_groups
import bank
import message_buffer


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

LINEAR_TOWER = 'LINEAR_TOWER'
THREE_SIXTY_TOWER = 'THREE_SIXTY_TOWER'
EXPLOSION_TOWER = 'EXPLOSION_TOWER'
TELEPORTATION_TOWER = 'TELEPORTATION_TOWER'


class Tower(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Towers"""

    def __init__(self, colour, position, dimension, buy_price, sell_price, initial_attack_values,
                 speed_upgrade_values_and_prices_and_icons, radius_upgrade_values_and_prices_and_icons,
                 pop_power_upgrade_values_and_prices_and_icons, tower_type, DISPLAYSURF):
        """
        :param colour: colour.COLOUR_CONSTANT, the colour of the icon
        :param position: 2-element tuple, where this icon is to be placed
        :param dimension: 2-element tuple, the size of this icon
        :param buy_price: int, the amount of money to withdraw from balance to create this tower
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        """

        assert isinstance(colour, tuple) and len(colour) == 4, 'colour must be a 4-element tuple'
        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(dimension, tuple) and len(dimension) == 2, 'start must be a 2-element tuple'
        assert isinstance(buy_price, int), 'buy_price must be an integer'
        assert isinstance(sell_price, int), 'buy_price must be an integer'
        assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame Surface object'

        super().__init__()

        self.DISPLAYSURF = DISPLAYSURF
        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.buy_price = buy_price
        self.sell_price = sell_price

        self._attack_values = initial_attack_values

        self._speed_upgrade_values_and_prices_and_icons = speed_upgrade_values_and_prices_and_icons
        self._radius_upgrade_values_and_prices_and_icons = radius_upgrade_values_and_prices_and_icons
        self._pop_power_upgrade_values_and_prices_and_icons = pop_power_upgrade_values_and_prices_and_icons
        self.frames_until_attack_again = self._attack_values.speed  # set the counter to the 'shoot' position

        self.tower_type = tower_type  # this is an enumerated string. We use this instead of type(...) to maintain consistency in specifying tower types
        self._pop_count = 0  # the number of balloons this tower popped

    def increment_pop_count(self, amount=1):
        self._pop_count += amount
        message_buffer.push_update_tower_pop_count_message(id(self), self._pop_count)


    def general_upgrade(self, upgrade_object):
        """
        :param upgrade_object: a type inheriting from Upgrade, eg, SpeedUpgrade
        :param attack_value: the attack value to change, eg, self._attack_values.spee
        """
        logger.debug('upgrade_speed called')
        if upgrade_object.is_next_upgrade_exists():
            # logger.debug('inside if for is_next_upgrade_exists')
            upgrade_value, upgrade_price = upgrade_object.get_next_upgrade_value_and_price()
            if bank.balance >= upgrade_price:  # if enough money in bank, change the appropriate attack value, withdraw the price from bank, increase sell price, remove existing icon and add new one
                # attack_value_to_upgrade = upgrade_value #Python function parameters are references, passed by value, thus, changing this here doesn't change self._....
                bank.withdraw(upgrade_price)
                self.sell_price += int(upgrade_price / 2)
                upgrade_object.update_upgrade_icon()
                return upgrade_value
        else:
            # create a placeholder icon
            self._speed_upgrade_values_and_prices_and_icons.update_with_placeholder_icon()

    def upgrade_speed(self):
        """
        :return: int, buy_price of next upgrade, so that a user can upgrade towers successively without reclicking on tower
        """
        # if there's an upgraded speed value make the current speed value to that one. Reason we're making general_upgrade return is because
        # passing in the self._attack_values.speed is passing the reference but by value, thus won't change self._attack_values.speed value
        upgraded_speed_value = self.general_upgrade(self._speed_upgrade_values_and_prices_and_icons)
        if upgraded_speed_value:
            self._attack_values.speed = upgraded_speed_value
            message_buffer.push_update_tower_speed_message(id(self), self._attack_values.speed)

    def upgrade_radius(self):
        """
        :return: int, buy_price of next upgrade, so that a user can upgrade towers successively without reclicking on tower
        """

        upgraded_radius_value = self.general_upgrade(self._radius_upgrade_values_and_prices_and_icons)
        if upgraded_radius_value:
            self._attack_values.radius = upgraded_radius_value
            message_buffer.push_update_tower_radius_message(id(self), self._attack_values.radius)

    def upgrade_pop_power(self):
        """
        :return: int, buy_price of next upgrade, so that a user can upgrade towers successively without reclicking on tower
        """

        upgraded_pop_power_value = self.general_upgrade(self._pop_power_upgrade_values_and_prices_and_icons)
        if upgraded_pop_power_value:
            self._attack_values.pop_power = upgraded_pop_power_value
            message_buffer.push_update_tower_pop_power_message(id(self), self._attack_values.pop_power)

    def sell_tower(self):
        """
        :return: int, the amount of money to be added to bank balance from selling this tower
        Destroys this tower and returns the price. Maybe this name is a bit misleading
        """
        self.kill()
        # logger.info(str(id(self)))
        message_buffer.push_sell_tower_message(id(self))
        # logger.debug('selling tower: the sell price is' + str(self.sell_price))
        bank.deposit(self.sell_price)

    def on_click(self, upgrade_icon_sprites, sell_tower_icon_sprite):
        """
        :param upgrade_icon_sprites: pygame.sprite.Group, contains all three upgrade icons in the game
        :return: None, upgrade_icon_sprites is changed here to include the three upgrade sprite
        Fills the upgrade_icon_sprite group with the upgrade icon sprites associated with this tower. If upgrade is already at max, show nothing
        """
        assert isinstance(upgrade_icon_sprites,
                          pygame.sprite.Group), 'upgrade_icon_sprites must be a pygame.sprite.Group() instance'

        upgrade_icon_sprites.empty()
        sell_tower_icon_sprite.empty()

        various_upgrades = [self._speed_upgrade_values_and_prices_and_icons,
                            self._radius_upgrade_values_and_prices_and_icons,
                            self._pop_power_upgrade_values_and_prices_and_icons]

        for i, upgrade in enumerate(various_upgrades):
            if upgrade.is_next_upgrade_exists():
                next_upgrade_icon = upgrade.get_next_upgrade_icon()
                upgrade_icon_sprites.add(next_upgrade_icon)
            else:
                upgrade_icon_sprites.add(icon.create_placeholder_upgrade_icon(position=((i + 1) * 100, 350), dimension=(
                    50, 50)))  # using (i+1) is coupling, consider changing later

        # create sell tower icon
        sell_tower_icon_sprite.add(icon.create_sell_tower_icon(self.sell_tower))

        return None

    @abc.abstractmethod
    def create_bullets(balloon):
        """Implemented by concrete towers to create and return the bullets needed"""
        pass

    def update(self, balloon_sprites, bullet_sprites):
        """
        :param balloon_sprites:
        :param bullet_sprites:
        :return:
        called every frame to whether whether to make bullets or not
        """
        assert isinstance(balloon_sprites, sprite_groups.BalloonGroup), "balloon_sprites must be a pygame.sprite.Group object"
        assert isinstance(bullet_sprites, pygame.sprite.Group), "bullet_sprites must be a pygame.sprite.Group object"

        pygame.draw.circle(self.DISPLAYSURF, colours.WHITE, (self.rect.centerx, self.rect.centery), self._attack_values.radius, 1)

        # checks if it's possible to attack again
        if self.frames_until_attack_again == self._attack_values.speed:
            for balloon in balloon_sprites:
                # if within range, create a bullet
                if math.hypot(balloon.get_centerX() - self.rect.centerx,
                              balloon.get_centerY() - self.rect.centery) <= self._attack_values.radius:
                    bullets = self.create_bullets(
                        balloon)  # create specific bullets, depending on tower, using Strategy pattern. Might only one bullet be created and returned

                    bullet_sprites.add(bullets)

                    self.frames_until_attack_again = 0
                    break
        else:
            self.frames_until_attack_again += 1


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

        initial_attack_values = AttackValues(initial_speed=10, initial_radius=50, initial_pop_power=1)

        speed_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_SPEED_ICONS, self.upgrade_speed)
        radius_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_RADIUS_ICONS, self.upgrade_radius)
        pop_power_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_POP_POWER_ICONS, self.upgrade_pop_power)

        speed_upgrade_values_and_prices_and_icons = SpeedUpgrade(speed_upgrade_values=(20, 30),
                                                                 speed_upgrade_prices=(20, 30),
                                                                 speed_upgrade_icons=speed_upgrade_icons)
        radius_upgrade_values_and_prices_and_icons = RadiusUpgrade(radius_upgrade_values=(60, 70),
                                                                   radius_upgrade_prices=(60, 70),
                                                                   radius_upgrade_icons=radius_upgrade_icons)
        pop_power_upgrade_values_and_prices_and_icons = PopPowerUpgrade(pop_power_upgrade_values=(2, 3),
                                                                        pop_power_upgrade_prices=(2, 3),
                                                                        pop_power_upgrade_icons=pop_power_upgrade_icons)

        super().__init__(colour=colours.YELLOW,
                         position=position,
                         dimension=(50, 50),
                         buy_price=10,
                         sell_price=5,
                         initial_attack_values=initial_attack_values,
                         speed_upgrade_values_and_prices_and_icons=speed_upgrade_values_and_prices_and_icons,
                         radius_upgrade_values_and_prices_and_icons=radius_upgrade_values_and_prices_and_icons,
                         pop_power_upgrade_values_and_prices_and_icons=pop_power_upgrade_values_and_prices_and_icons,
                         tower_type=LINEAR_TOWER,
                         DISPLAYSURF=DISPLAYSURF)

    def create_bullets(self, balloon):
        """
        :param balloon:
        :return: bullet
        Creates a bullet directed towards the given balloon
        """
        return bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                    start=(self.rect.centerx, self.rect.centery),
                                    destination=(balloon.get_centerX(), balloon.get_centerY()),
                                    pop_power=self._attack_values.pop_power,
                                    tower_increment_pop_method=self.increment_pop_count)


class ThreeSixtyTower(Tower):
    def __init__(self, position, DISPLAYSURF):
        """
        :param position: 2-element tuple, where this icon is to be placed
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        Creates a ThreeSixtyTower (shoots 8 StandardBullets)
        """

        assert isinstance(position, tuple) and len(position) == 2, 'destination must be a 2-element tuple'
        assert isinstance(DISPLAYSURF, pygame.Surface), 'DISPLAYSURF must be a pygame Surface object'

        initial_attack_values = AttackValues(initial_speed=10, initial_radius=50, initial_pop_power=1)

        speed_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_SPEED_ICONS, self.upgrade_speed)
        radius_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_RADIUS_ICONS, self.upgrade_radius)
        pop_power_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_POP_POWER_ICONS, self.upgrade_pop_power)

        speed_upgrade_values_and_prices_and_icons = SpeedUpgrade(speed_upgrade_values=(20, 30),
                                                                 speed_upgrade_prices=(20, 30),
                                                                 speed_upgrade_icons=speed_upgrade_icons)
        radius_upgrade_values_and_prices_and_icons = RadiusUpgrade(radius_upgrade_values=(60, 70),
                                                                   radius_upgrade_prices=(60, 70),
                                                                   radius_upgrade_icons=radius_upgrade_icons)
        pop_power_upgrade_values_and_prices_and_icons = PopPowerUpgrade(pop_power_upgrade_values=(2, 3),
                                                                        pop_power_upgrade_prices=(2, 3),
                                                                        pop_power_upgrade_icons=pop_power_upgrade_icons)

        super().__init__(colour=colours.CYAN,
                         position=position,
                         dimension=(40, 40),
                         buy_price=20,
                         sell_price=10,
                         initial_attack_values=initial_attack_values,
                         speed_upgrade_values_and_prices_and_icons=speed_upgrade_values_and_prices_and_icons,
                         radius_upgrade_values_and_prices_and_icons=radius_upgrade_values_and_prices_and_icons,
                         pop_power_upgrade_values_and_prices_and_icons=pop_power_upgrade_values_and_prices_and_icons,
                         tower_type=THREE_SIXTY_TOWER,
                         DISPLAYSURF=DISPLAYSURF)

    def create_bullets(self, balloons):
        return [bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx, self.rect.centery - 100),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx + 100, self.rect.centery - 100),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx + 100, self.rect.centery),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx + 100, self.rect.centery + 100),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx, self.rect.centery + 100),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx - 100, self.rect.centery + 100),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx - 100, self.rect.centery),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count),

                bullet.create_bullet(bullet_type=bullet.STANDARD_BULLET,
                                     start=(self.rect.centerx, self.rect.centery),
                                     destination=(self.rect.centerx - 100, self.rect.centery - 100),
                                     pop_power=self._attack_values.pop_power,
                                     tower_increment_pop_method=self.increment_pop_count)
                ]


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

        initial_attack_values = AttackValues(initial_speed=10, initial_radius=50, initial_pop_power=1)

        speed_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_SPEED_ICONS, self.upgrade_speed)
        radius_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_RADIUS_ICONS, self.upgrade_radius)
        pop_power_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_POP_POWER_ICONS, self.upgrade_pop_power)

        speed_upgrade_values_and_prices_and_icons = SpeedUpgrade(speed_upgrade_values=(20, 30),
                                                                 speed_upgrade_prices=(20, 30),
                                                                 speed_upgrade_icons=speed_upgrade_icons)
        radius_upgrade_values_and_prices_and_icons = RadiusUpgrade(radius_upgrade_values=(60, 70),
                                                                   radius_upgrade_prices=(60, 70),
                                                                   radius_upgrade_icons=radius_upgrade_icons)
        pop_power_upgrade_values_and_prices_and_icons = PopPowerUpgrade(pop_power_upgrade_values=(2, 3),
                                                                        pop_power_upgrade_prices=(2, 3),
                                                                        pop_power_upgrade_icons=pop_power_upgrade_icons)

        super().__init__(colour=colours.WHITE,
                         position=position,
                         dimension=(40, 40),
                         buy_price=30,
                         sell_price=15,
                         initial_attack_values=initial_attack_values,
                         speed_upgrade_values_and_prices_and_icons=speed_upgrade_values_and_prices_and_icons,
                         radius_upgrade_values_and_prices_and_icons=radius_upgrade_values_and_prices_and_icons,
                         pop_power_upgrade_values_and_prices_and_icons=pop_power_upgrade_values_and_prices_and_icons,
                         tower_type=EXPLOSION_TOWER,
                         DISPLAYSURF=DISPLAYSURF)

    def create_bullets(self, balloon):
        return bullet.create_bullet(bullet_type=bullet.EXPLOSION_BULLET,
                                    start=(self.rect.centerx, self.rect.centery),
                                    destination=(balloon.get_centerX(), balloon.get_centerY()),
                                    pop_power=self._attack_values.pop_power,
                                    tower_increment_pop_method=self.increment_pop_count)


class TeleportationTower(Tower):
    """Shoots TeleportationBullets"""

    def __init__(self, position, DISPLAYSURF):
        """
        :param position: 2-element tuple, where this icon is to be placed
        :param DISPLAYSURF: main Surface object, for displaying this tower's circle
        Creates a TeleportationTower (shoots TeleportationBullets)
        """
        initial_attack_values = AttackValues(initial_speed=10, initial_radius=50, initial_pop_power=1)

        speed_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_SPEED_ICONS, self.upgrade_speed)
        radius_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_RADIUS_ICONS, self.upgrade_radius)
        pop_power_upgrade_icons = icon.create_upgrade_type_icons_batch(icon.UPGRADE_POP_POWER_ICONS, self.upgrade_pop_power)

        speed_upgrade_values_and_prices_and_icons = SpeedUpgrade(speed_upgrade_values=(20, 30),
                                                                 speed_upgrade_prices=(20, 30),
                                                                 speed_upgrade_icons=speed_upgrade_icons)
        radius_upgrade_values_and_prices_and_icons = RadiusUpgrade(radius_upgrade_values=(60, 70),
                                                                   radius_upgrade_prices=(60, 70),
                                                                   radius_upgrade_icons=radius_upgrade_icons)
        pop_power_upgrade_values_and_prices_and_icons = PopPowerUpgrade(pop_power_upgrade_values=(2, 3),
                                                                        pop_power_upgrade_prices=(2, 3),
                                                                        pop_power_upgrade_icons=pop_power_upgrade_icons)
        super().__init__(colour=colours.BROWN,
                         position=position,
                         dimension=(40, 40),
                         buy_price=40,
                         sell_price=20,
                         initial_attack_values=initial_attack_values,
                         speed_upgrade_values_and_prices_and_icons=speed_upgrade_values_and_prices_and_icons,
                         radius_upgrade_values_and_prices_and_icons=radius_upgrade_values_and_prices_and_icons,
                         pop_power_upgrade_values_and_prices_and_icons=pop_power_upgrade_values_and_prices_and_icons,
                         tower_type=TELEPORTATION_TOWER,
                         DISPLAYSURF=DISPLAYSURF)

    def create_bullets(self, balloon):
        return bullet.create_bullet(bullet_type=bullet.TELEPORTATION_BULLET,
                                    start=(self.rect.centerx, self.rect.centery),
                                    destination=(balloon.get_centerX(), balloon.get_centerY()),
                                    pop_power=self._attack_values.pop_power,
                                    tower_increment_pop_method=self.increment_pop_count)


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


class AttackValues:
    def __init__(self, initial_speed, initial_radius, initial_pop_power):
        """initializes the attack properties of this tower"""
        self.speed = initial_speed
        self.radius = initial_radius
        self.pop_power = initial_pop_power


class Upgrade:
    """Base class for all upgrades, include speed, radius, and pop_power"""

    def __init__(self, upgrade_values, upgrade_prices, upgrade_icons):
        """
        :param upgrade_values: a tuple containing the values associated with the specific upgrade
        :param upgrade_prices: a tuple containing the prices associated with the specific upgrade
        Sets the upgrade values and prices for them
        """

        assert len(upgrade_values) == len(upgrade_prices), 'the length of upgrade values and prices must be the same'

        self._upgrade_values = upgrade_values  # consider zipping these together?
        self._upgrade_prices = upgrade_prices
        self._upgrade_icons = upgrade_icons

        self.next_upgrade_index = 0  # represents the index of the next upgrade value and prices
        self.total_number_of_upgrade = len(upgrade_values)

    def is_next_upgrade_exists(self):
        if self.next_upgrade_index == self.total_number_of_upgrade:  # the largest value of the upgrade index is 1 less than total number of upgrades
            return False
        return True

    def get_next_upgrade_value_and_price(self):
        next_upgrade_value = self._upgrade_values[self.next_upgrade_index]
        next_upgrade_price = self._upgrade_prices[self.next_upgrade_index]

        return next_upgrade_value, next_upgrade_price

    def get_next_upgrade_icon(self):
        """returns the upgrade icon that is to be shown"""
        next_upgrade_icon = self._upgrade_icons[self.next_upgrade_index]
        return next_upgrade_icon

    def update_upgrade_icon(self):
        """change the upgrade icon to the next one (not placeholder icon. No need to error check because the user is presumed to have checked is_next_upgrade_exist. This is the final stage of updating
        and the upgrade_index will increment"""

        # remove current icon
        sprite_groups.upgrade_icon_sprites.remove(self._upgrade_icons[self.next_upgrade_index])

        self.next_upgrade_index += 1
        if self.is_next_upgrade_exists():
            # add new icon
            sprite_groups.upgrade_icon_sprites.add(self._upgrade_icons[self.next_upgrade_index])
        else:
            self.update_with_placeholder_icon()

    def update_with_placeholder_icon(self):
        """change the current upgrade icon with a placeholder icon"""

        position = (
            self._upgrade_icons[0].rect.centerx, self._upgrade_icons[
                0].rect.centery)  # this is hacky but works because all speed icons (or radius icons or pop_powers) have same position

        # remove current icon
        sprite_groups.upgrade_icon_sprites.remove(self._upgrade_icons[
                                                      self.next_upgrade_index - 1])  # very hacky, what the heck is going on with the value of next_upgrade_index? What does it represent?

        # add placeholder icon
        sprite_groups.upgrade_icon_sprites.add(icon.create_placeholder_upgrade_icon(position=position, dimension=(50, 50)))


class SpeedUpgrade(Upgrade):
    """Represents the upgrade values and prices for a tower's attack speed"""

    def __init__(self, speed_upgrade_values, speed_upgrade_prices, speed_upgrade_icons):
        super().__init__(speed_upgrade_values, speed_upgrade_prices, speed_upgrade_icons)


class RadiusUpgrade(Upgrade):
    """Represents the upgrade values and prices for a tower's radius"""

    def __init__(self, radius_upgrade_values, radius_upgrade_prices, radius_upgrade_icons):
        super().__init__(radius_upgrade_values, radius_upgrade_prices, radius_upgrade_icons)


class PopPowerUpgrade(Upgrade):
    """Represents the upgrade values and prices for a tower's pop power"""

    def __init__(self, pop_power_upgrade_values, pop_power_upgrade_prices, pop_power_upgrade_icons):
        super().__init__(pop_power_upgrade_values, pop_power_upgrade_prices, pop_power_upgrade_icons)
