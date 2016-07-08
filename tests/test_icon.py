import unittest
from unittest.mock import Mock
from unittest.mock import patch

import icon
import colours
import tower
import logging


class TestIcon(unittest.TestCase):
    @patch.multiple(icon.Icon, __abstractmethods__=set())
    def test_init(self):
        colour = colours.GREEN
        position = (10, 20)
        dimension = (50, 60)

        i = icon.Icon(colour, position, dimension)

        self.assertEqual(i.image.get_width(), 50)
        self.assertEqual(i.image.get_height(), 60)
        self.assertEqual(i.image.get_at((5, 5)), (0, 255, 0, 255))
        self.assertEqual(i.rect.centerx, 10)
        self.assertEqual(i.rect.centery, 20)

    @patch.multiple(icon.Icon, __abstractmethods__=set())
    def test_update(self):
        colour = colours.GREEN
        position = (10, 20)
        dimension = (50, 60)

        i = icon.Icon(colour, position, dimension)
        mouse_position = (120, 130)
        i.update(mouse_position)

        self.assertEqual(i.rect.centerx, 120)
        self.assertEqual(i.rect.centery, 130)


class TestTowerIcon(unittest.TestCase):
    @patch.multiple(icon.TowerIcon, __abstractmethods__=set())
    @patch.object(icon.Icon, '__init__')
    def test_init(self, mock_icon_init):
        colour = (255, 255, 255, 255)
        position = (35, 25)
        dimension = (40, 40)
        t = icon.TowerIcon(colour, position, dimension)
        mock_icon_init.called_with(colour, position, dimension)


class TestLinearTowerIcon(unittest.TestCase):
    def test_init(self):
        colour = colours.GREEN
        position = (10, 20)
        dimension = (50, 60)

        i = icon.LinearTowerIcon(colour, position, dimension)

        self.assertEqual(i._tower_type, tower.LINEAR_TOWER)

    def test_on_left_mouse_button(self):
        colour = colours.GREEN
        position = (10, 20)
        dimension = (50, 60)

        i = icon.LinearTowerIcon(colour, position, dimension)
        i.on_left_mouse_button_up()
        self.assertEqual(i.image.get_at((15, 25)), (255, 165, 0, 255))

    def test_duplicate(self):
        colour = colours.GREEN
        position = (10, 20)
        dimension = (50, 60)

        i = icon.LinearTowerIcon(colour, position, dimension)
        return_value = i.duplicate()

        self.assertIsInstance(return_value, icon.LinearTowerIcon)


class TestThreeSixtyTowerIcon(unittest.TestCase):
    def setUp(self):
        self.colour = colours.GREEN
        self.position = (10, 20)
        self.dimension = (50, 60)

        self.i = icon.ThreeSixtyTowerIcon(self.colour, self.position, self.dimension)

    def test_init(self):
        self.assertEqual(self.i._tower_type, tower.THREE_SIXTY_TOWER)

    def test_on_left_mouse_button(self):
        self.i.on_left_mouse_button_up()
        self.assertEqual(self.i.image.get_at((10, 25)), (255, 165, 0, 255))

    def test_duplicate(self):
        return_value = self.i.duplicate()

        self.assertIsInstance(return_value, icon.ThreeSixtyTowerIcon)


class TestExplosionTowerIcon(unittest.TestCase):
    def setUp(self):
        self.colour = colours.GREEN
        self.position = (10, 20)
        self.dimension = (50, 60)

        self.i = icon.ExplosionTowerIcon(self.colour, self.position, self.dimension)

    def test_init(self):
        self.assertEqual(self.i._tower_type, tower.EXPLOSION_TOWER)

    def test_on_left_mouse_button(self):
        self.i.on_left_mouse_button_up()
        self.assertEqual(self.i.image.get_at((15, 25)), (255, 165, 0, 255))

    def test_duplicate(self):
        return_value = self.i.duplicate()

        self.assertIsInstance(return_value, icon.ExplosionTowerIcon)


class TestTeleportationTowerIcon(unittest.TestCase):
    def setUp(self):
        self.colour = colours.GREEN
        self.position = (10, 20)
        self.dimension = (50, 60)

        self.i = icon.TeleportationTowerIcon(self.colour, self.position, self.dimension)

    def test_init(self):
        self.assertEqual(self.i._tower_type, tower.TELEPORTATION_TOWER)

    def test_on_left_mouse_button(self):
        self.i.on_left_mouse_button_up()
        self.assertEqual(self.i.image.get_at((5, 5)), (255, 165, 0, 255))

    def test_duplicate(self):
        return_value = self.i.duplicate()

        self.assertIsInstance(return_value, icon.TeleportationTowerIcon)


class TestUpgradeIcon(unittest.TestCase):
    @patch.multiple(icon.UpgradeIcon, __abstractmethods__=set())
    @patch.object(icon.Icon, '__init__')
    def test_init(self, mock_icon_init):
        colour = (255, 255, 255, 255)
        position = (35, 25)
        dimension = (40, 40)
        t = icon.UpgradeIcon(colour, position, dimension)
        mock_icon_init.called_with(colour, position, dimension)


class TestUpgradeSpeedIcon(unittest.TestCase):
    def setUp(self):
        self.colour = colours.GREEN
        self.position = (10, 20)
        self.dimension = (50, 60)

        self.u = icon.UpgradeSpeedIcon(self.colour, self.position, self.dimension)

    @patch.object(icon.UpgradeIcon, '__init__')
    def test_init(self, mock_upgrade_icon_init):
        self.u = icon.UpgradeSpeedIcon(self.colour, self.position, self.dimension)
        mock_upgrade_icon_init.called_with(self.colour, self.position, self.dimension)

    @patch.object(logging.Logger, 'info')
    def test_on_left_mouse_button(self, mock_logger_info):
        self.u.on_left_mouse_button_up()
        self.assertEqual(mock_logger_info.call_count, 1)


class TestUpgradeRadiusIcon(unittest.TestCase):
    def setUp(self):
        self.colour = colours.GREEN
        self.position = (10, 20)
        self.dimension = (50, 60)

        self.u = icon.UpgradeRadiusIcon(self.colour, self.position, self.dimension)

    @patch.object(icon.UpgradeIcon, '__init__')
    def test_init(self, mock_upgrade_icon_init):
        self.u = icon.UpgradeRadiusIcon(self.colour, self.position, self.dimension)
        mock_upgrade_icon_init.called_with(self.colour, self.position, self.dimension)

    @patch.object(logging.Logger, 'info')
    def test_on_left_mouse_button(self, mock_logger_info):
        self.u.on_left_mouse_button_up()
        self.assertEqual(mock_logger_info.call_count, 1)


class TestUpgradePopPowerIcon(unittest.TestCase):
    def setUp(self):
        self.colour = colours.GREEN
        self.position = (10, 20)
        self.dimension = (50, 60)

        self.u = icon.UpgradePopPowerIcon(self.colour, self.position, self.dimension)

    @patch.object(icon.UpgradeIcon, '__init__')
    def test_init(self, mock_upgrade_icon_init):
        self.u = icon.UpgradePopPowerIcon(self.colour, self.position, self.dimension)
        mock_upgrade_icon_init.called_with(self.colour, self.position, self.dimension)

    @patch.object(logging.Logger, 'info')
    def test_on_left_mouse_button(self, mock_logger_info):
        self.u.on_left_mouse_button_up()
        self.assertEqual(mock_logger_info.call_count, 1)


class TestIconModule(unittest.TestCase):
    def test_tower_icon_type_with_LINEAR_TOWER_ICON(self):
        icon_type = icon.LINEAR_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_tower_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.LinearTowerIcon)

    def test_tower_icon_type_with_THREE_SIXTY_TOWER_ICON(self):
        icon_type = icon.THREE_SIXTY_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_tower_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.ThreeSixtyTowerIcon)

    def test_tower_icon_type_with_EXPLOSION_TOWER_TYPE(self):
        icon_type = icon.EXPLOSION_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_tower_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.ExplosionTowerIcon)

    def test_tower_icon_type_with_TELEPORTATION_TOWER_TYPE(self):
        icon_type = icon.TELEPORTATION_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_tower_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.TeleportationTowerIcon)

    def test_tower_icon_type_with_invalid_type(self):
        icon_type = 'invalid icon type'
        position = (100, 100)

        self.assertRaises(NotImplementedError, icon.create_tower_icon, icon_type, position)

    @patch.object(icon.UpgradeSpeedIcon, '__init__')
    def test_upgrade_icon_type_with_UPGRADE_SPEED_ICON_TYPE(self, mock_upgrade_speed_icon):
        icon_type = icon.UPGRADE_SPEED_ICON
        mock_upgrade_speed_icon.return_value = None
        icon.create_upgrade_icon(icon_type)

        mock_upgrade_speed_icon.assert_called_with(colour=colours.WHITE, position=(100, 350), dimension=(50, 50))

    @patch.object(icon.UpgradeRadiusIcon, '__init__')
    def test_upgrade_icon_type_with_UPGRADE_RADIUS_ICON_TYPE(self, mock_upgrade_speed_icon):
        icon_type = icon.UPGRADE_RADIUS_ICON
        mock_upgrade_speed_icon.return_value = None

        icon.create_upgrade_icon(icon_type)

        mock_upgrade_speed_icon.assert_called_with(colour=colours.WHITE, position=(200, 350), dimension=(50, 50))


    @patch.object(icon.UpgradePopPowerIcon, '__init__')
    def test_upgrade_icon_type_with_UPGRADE_POP_POWER_ICON_TYPE(self, mock_upgrade_speed_icon):
        icon_type = icon.UPGRADE_POP_POWER_ICON
        mock_upgrade_speed_icon.return_value = None

        icon.create_upgrade_icon(icon_type)

        mock_upgrade_speed_icon.assert_called_with(colour=colours.WHITE, position=(300, 350), dimension=(50, 50))


    def test_upgrade_icon_type_with_invalid_type(self):
        icon_type = 'invalid icon type'

        self.assertRaises(NotImplementedError, icon.create_upgrade_icon, icon_type)