import unittest
from unittest.mock import Mock
from unittest.mock import patch

import icon
import colours
import tower
import sprite_groups
import pygame
import math
import bullet
import logging


class TestTower(unittest.TestCase):
    @patch.multiple(tower.Tower, __abstractmethods__=set())
    def setUp(self):
        self.color = (0, 0, 255)
        self.position = (15, 25)
        self.dimension = (80, 90)
        self.attack_radius = 10
        self.cost = 60
        self.DISPLAYSURF = pygame.Surface([150, 160])

        self.t = tower.Tower(self.color, self.position, self.dimension, self.cost, self.DISPLAYSURF)

    @patch.object(pygame.draw, 'circle')
    @patch.multiple(tower.Tower, __abstractmethods__=set())
    def test_init(self, mock_pygame_draw_circle):
        self.t = tower.Tower(self.color, self.position, self.dimension, self.cost, self.DISPLAYSURF)

        self.assertEqual(self.t.DISPLAYSURF, self.DISPLAYSURF)
        self.assertEqual(self.t.image.get_width(), 80)
        self.assertEqual(self.t.image.get_height(), 90)
        self.assertEqual(self.t.image.get_at((5, 5)), (0, 0, 255, 255))
        self.assertEqual(self.t.rect.centerx, 15)
        self.assertEqual(self.t.rect.centery, 25)




class TestLinearTower(unittest.TestCase):
    def setUp(self):
        self.position = (15, 25)
        self.attack_radius = 80
        self.DISPLAYSURF = pygame.Surface([150, 160])

        self.t = tower.LinearTower(self.position, self.DISPLAYSURF)

    @patch.object(tower.Tower, '__init__')
    def test_init(self, mock_tower_init):

        self.t = tower.LinearTower(self.position, self.DISPLAYSURF)
        self.t._attk_props.speed = 15

        mock_tower_init.assert_called_with(colour=colours.YELLOW, position=self.position, dimension=(50, 50),
                                           cost=10, DISPLAYSURF=self.DISPLAYSURF)
        self.assertEqual(self.t._attack_again_counter, 10)



    @patch.object(pygame.draw, 'circle')
    def test_update_with_not_time_to_attack(self, mock_pygame_draw_circle):
        self.t._attk_props.speed = 5
        self.t._attack_again_counter = 7
        self.t.update('fake_ballon_sprites', 'fake_bullet_sprites')

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.attack_radius, 1)
        self.assertEqual(self.t._attack_again_counter, 8)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_within_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                     mock_sprite_group_add, mock_bullet_create_bullet):
        self.t._attack_again_counter = 10
        self.t._attk_props.radius = 70
        self.t._attk_props.pop_power = 3

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 60

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 1)
        self.assertEqual(mock_bullet_create_bullet.call_count, 1)
        mock_bullet_create_bullet.assert_called_with(bullet.STANDARD_BULLET, start=self.position, destination=(20, 30), pop_power=self.t._attk_props.pop_power)
        self.assertEqual(self.t._attack_again_counter, 0)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_outside_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                      mock_sprite_group_add, mock_bullet_create_bullet):
        self.t._attack_again_counter = 10
        self.t._attk_props.radius  = 70

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t._attack_again_counter, 10)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_without_ballon(self, mock_pygame_draw_circle, mock_math_hypot,
                                                       mock_sprite_group_add, mock_bullet_create_bullet):
        self.t._attack_again_counter = 10
        self.t._attk_props.radius = 70

        balloon_sprites = []
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t._attack_again_counter, 10)

    def test_handle_is_clicked(self):
        upgrade_icon_sprites = Mock(spec=pygame.sprite.Group)
        self.t.handle_is_clicked(upgrade_icon_sprites)

        self.assertEqual(upgrade_icon_sprites.add.call_count, 3)

class TestThreeSixtyTower(unittest.TestCase):
    def setUp(self):
        self.position = (15, 25)
        self.attack_radius = 60
        self.DISPLAYSURF = pygame.Surface([150, 160])

        self.t = tower.ThreeSixtyTower(self.position, self.DISPLAYSURF)

    @patch.object(tower.Tower, '__init__')
    def test_init(self, mock_tower_init):
        self.t = tower.ThreeSixtyTower(self.position, self.DISPLAYSURF)

        mock_tower_init.assert_called_with(colour=colours.CYAN, position=self.position, dimension=(40, 40),
                                           cost=20,  DISPLAYSURF=self.DISPLAYSURF)

    @patch.object(pygame.draw, 'circle')
    def test_update_with_not_time_to_attack(self, mock_pygame_draw_circle):
        self.t._attack_again_counter = 5
        self.t.update('fake_ballon_sprites', 'fake_bullet_sprites')

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)
        self.assertEqual(self.t._attack_again_counter, 6)



    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_within_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                     mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t._attk_props.radius = 70
        self.t._attk_props.pop_power = 3

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 60

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 1)
        self.assertEqual(mock_bullet_create_bullet.call_count, 8)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(15, -75), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(115, -75), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(115, 25), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(115, 125), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(15, 125), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(-85, 125), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(-85, 25), pop_power=3)
        mock_bullet_create_bullet.assert_any_call(bullet.STANDARD_BULLET, start=self.position, destination=(-85, -75), pop_power=3)
        self.assertEqual(self.t.attack_again_counter, 0)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_outside_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                      mock_sprite_group_add, mock_bullet_create_bullet):
        self.t._attack_again_counter = 10
        self.t._attk_props.radius = 70
        self.t._attk_props.speed = 10

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t._attack_again_counter, 10)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_without_ballon(self, mock_pygame_draw_circle, mock_math_hypot,
                                                       mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t._attk_props.radius = 70

        balloon_sprites = []
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   70, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t.attack_again_counter, 10)

    def test_handle_is_clicked(self):
        upgrade_icon_sprites = Mock(spec=pygame.sprite.Group)
        self.t.handle_is_clicked(upgrade_icon_sprites)

        self.assertEqual(upgrade_icon_sprites.add.call_count, 3)


class TestExplosionTower(unittest.TestCase):
    def setUp(self):
        self.position = (15, 25)
        self.attack_radius = 70
        self.DISPLAYSURF = pygame.Surface([150, 160])

        self.t = tower.ExplosionTower(self.position, self.DISPLAYSURF)

    @patch.object(tower.Tower, '__init__')
    def test_init(self, mock_tower_init):
        self.t = tower.ExplosionTower(self.position, self.DISPLAYSURF)

        mock_tower_init.assert_called_with(colour=colours.WHITE, position=self.position, dimension=(40, 40),
                                           cost=30, DISPLAYSURF=self.DISPLAYSURF)

    @patch.object(pygame.draw, 'circle')
    def test_update_with_not_time_to_attack(self, mock_pygame_draw_circle):
        self.t.attack_again_counter = 5
        self.t._attk_props.speed = 10
        self.t.update('fake_ballon_sprites', 'fake_bullet_sprites')

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)
        self.assertEqual(self.t._attack_again_counter, 6)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_within_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                     mock_sprite_group_add, mock_bullet_create_bullet):
        self.t._attack_again_counter = 10
        self.t._attk_props.radius = 70
        self.t._attk_props.pop_power = 1

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 60

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 1)
        self.assertEqual(mock_bullet_create_bullet.call_count, 1)
        mock_bullet_create_bullet.assert_called_with(bullet.EXPLOSION_BULLET, start=self.position, destination=(20, 30), pop_power=1)
        self.assertEqual(self.t._attack_again_counter, 0)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_outside_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                      mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t._attk_props.radius = 70

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t.attack_again_counter, 10)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_without_ballon(self, mock_pygame_draw_circle, mock_math_hypot,
                                                       mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t._attk_props.radius = 70

        balloon_sprites = []
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t.attack_again_counter, 10)

    def test_handle_is_clicked(self):
        upgrade_icon_sprites = Mock(spec=pygame.sprite.Group)
        self.t.handle_is_clicked(upgrade_icon_sprites)

        self.assertEqual(upgrade_icon_sprites.add.call_count, 3)


class TestTeleportationTower(unittest.TestCase):
    def setUp(self):
        self.position = (15, 25)
        self.attack_radius = 100
        self.DISPLAYSURF = pygame.Surface([150, 160])

        self.t = tower.TeleportationTower(self.position, self.DISPLAYSURF)

    @patch.object(tower.Tower, '__init__')
    def test_init(self, mock_tower_init):
        self.t = tower.TeleportationTower(self.position, self.DISPLAYSURF)
        self.t._attk_props.radius = 15

        mock_tower_init.assert_called_with(colour=colours.BROWN, position=self.position, dimension=(40, 40),
                                           DISPLAYSURF=self.DISPLAYSURF, cost=40)

    @patch.object(pygame.draw, 'circle')
    def test_update_with_not_time_to_attack(self, mock_pygame_draw_circle):
        self.t._attack_again_counter = 5
        self.t.update('fake_ballon_sprites', 'fake_bullet_sprites')

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255),
                                                   self.position, self.t._attk_props.radius, 1)

        self.assertEqual(self.t._attack_again_counter, 6)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_within_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                     mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t.attack_radius = 70
        self.t._attk_props.radius = 30

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 60

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 1)
        self.assertEqual(mock_bullet_create_bullet.call_count, 1)
        mock_bullet_create_bullet.assert_called_with(bullet.TELEPORTATION_BULLET, start=self.position, destination=(20, 30))
        self.assertEqual(self.t.attack_again_counter, 0)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_with_ballon_and_outside_range(self, mock_pygame_draw_circle, mock_math_hypot,
                                                                      mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t.attack_radius = 70
        self.t._attk_props.radius = 30

        mock_balloon = Mock()
        mock_balloon.get_centerX.return_value = 20
        mock_balloon.get_centerY.return_value = 30

        balloon_sprites = [mock_balloon]
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t.attack_again_counter, 10)

    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(math, 'hypot')
    @patch.object(pygame.draw, 'circle')
    def test_update_with_time_to_attack_without_ballon(self, mock_pygame_draw_circle, mock_math_hypot,
                                                       mock_sprite_group_add, mock_bullet_create_bullet):
        self.t.attack_again_counter = 10
        self.t.attack_radius = 70
        self.t._attk_props.radius = 30

        balloon_sprites = []
        bullet_sprites = sprite_groups.bullet_sprites
        mock_math_hypot.return_value = 80

        self.t.update(balloon_sprites, bullet_sprites)

        mock_pygame_draw_circle.assert_called_with(self.DISPLAYSURF, (255, 255, 255, 255), self.position,
                                                   self.t._attk_props.radius, 1)

        self.assertEqual(mock_sprite_group_add.call_count, 0)
        self.assertEqual(mock_bullet_create_bullet.call_count, 0)
        self.assertEqual(self.t.attack_again_counter, 10)

    def test_handle_is_clicked(self):
        upgrade_icon_sprites = Mock(spec=pygame.sprite.Group)
        self.t.handle_is_clicked(upgrade_icon_sprites)

        self.assertEqual(upgrade_icon_sprites.add.call_count, 3)


class TestTowerModule(unittest.TestCase):
    def setUp(self):
        self.position = (100, 100)
        self.DISPLAYSURF = pygame.Surface([50, 50])

    def test_create_tower_with_LINEAR_TOWER_type(self):
        tower_type = tower.LINEAR_TOWER
        return_value = tower.create_tower(tower_type, self.position, self.DISPLAYSURF)

        self.assertIsInstance(return_value, tower.LinearTower)

    def test_create_tower_with_THREE_SIXTY_TOWER_type(self):
        tower_type = tower.THREE_SIXTY_TOWER
        return_value = tower.create_tower(tower_type, self.position, self.DISPLAYSURF)

        self.assertIsInstance(return_value, tower.ThreeSixtyTower)

    def test_create_tower_with_EXPLOSION_TOWER_type(self):
        tower_type = tower.EXPLOSION_TOWER
        return_value = tower.create_tower(tower_type, self.position, self.DISPLAYSURF)

        self.assertIsInstance(return_value, tower.ExplosionTower)

    def test_create_tower_with_TELEPORTATION_TOWER_type(self):
        tower_type = tower.TELEPORTATION_TOWER
        return_value = tower.create_tower(tower_type, self.position, self.DISPLAYSURF)

        self.assertIsInstance(return_value, tower.TeleportationTower)

    def test_create_tower_with_invalid_type(self):
        tower_type = 'invalid tower type'

        self.assertRaises(NotImplementedError, tower.create_tower, tower_type, self.position, self.DISPLAYSURF)
