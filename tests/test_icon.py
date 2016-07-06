import unittest
from unittest.mock import Mock
from unittest.mock import patch

import icon
import colours
import tower

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

class TestLinearTowerIcon(unittest.TestCase):

    def test_init(self):
        colour = colours.GREEN
        position = (10, 20)
        dimension = (50, 60)

        i = icon.LinearTowerIcon(colour, position, dimension)

        self.assertEqual(i.tower_type, tower.LINEAR_TOWER)

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
       self.assertEqual(self.i.tower_type, tower.THREE_SIXTY_TOWER)

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
       self.assertEqual(self.i.tower_type, tower.EXPLOSION_TOWER)

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
       self.assertEqual(self.i.tower_type, tower.TELEPORTATION_TOWER)

    def test_on_left_mouse_button(self):
        self.i.on_left_mouse_button_up()
        self.assertEqual(self.i.image.get_at((5, 5)), (255, 165, 0, 255))

    def test_duplicate(self):
        return_value = self.i.duplicate()

        self.assertIsInstance(return_value, icon.TeleportationTowerIcon)

class TestIconModule(unittest.TestCase):
    def test_icon_type_with_LINEAR_TOWER_ICON(self):
        icon_type = icon.LINEAR_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.LinearTowerIcon)

    def test_icon_type_with_THREE_SIXTY_TOWER_ICON(self):
        icon_type = icon.THREE_SIXTY_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.ThreeSixtyTowerIcon)

    def test_icon_type_with_EXPLOSION_TOWER_TYPE(self):
        icon_type = icon.EXPLOSION_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.ExplosionTowerIcon)

    def test_icon_type_with_TELEPORTATION_TOWER_TYPE(self):
        icon_type = icon.TELEPORTATION_TOWER_ICON
        position = (100, 100)
        return_value = icon.create_icon(icon_type, position)

        self.assertIsInstance(return_value, icon.TeleportationTowerIcon)

    def test_icon_type_with_invalid_type(self):
        icon_type = 'invalid icon type'
        position = (100, 100)

        self.assertRaises(NotImplementedError, icon.create_icon, icon_type, position)



