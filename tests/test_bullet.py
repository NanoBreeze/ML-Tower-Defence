import unittest
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
import bullet
import sprite_groups
import pygame
import colours
import balloon


class TestBullet(TestCase):
    @patch.object(pygame.sprite.AbstractGroup, 'add')
    @patch.multiple(bullet.Bullet, __abstractmethods__=set())
    def test_init_with_default_parameters(self, mock_ballon_group_add):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1

        b = bullet.Bullet(start, destination, pop_power)

        self.assertEqual(b.image.get_width(), 10)
        self.assertEqual(b.image.get_height(), 10)
        self.assertEqual(b.image.get_at((5, 5)), (0, 255, 0, 255))
        self.assertEqual(b.rect.centerx, 10)
        self.assertEqual(b.rect.centery, 20)
        self.assertEqual(b.destination_x, 40)
        self.assertEqual(b.destination_y, 60)
        self.assertEqual(b.frame_destroy_after, 5)
        self.assertEqual(b.frame_to_hit_Ballon, 2.5)
        self.assertEqual(b.step_x, 12)
        self.assertEqual(b.step_y, 16)
        self.assertEqual(mock_ballon_group_add.call_count, 1)

    @patch.object(pygame.sprite.AbstractGroup, 'add')
    @patch.multiple(bullet.Bullet, __abstractmethods__=set())
    def test_init_with_custom_parameters(self, mock_ballon_group_add):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1
        frame_destroy_after = 10
        dimension = (12, 13)
        colour = colours.BLUE

        b = bullet.Bullet(start, destination, pop_power, frame_destroy_after, dimension, colour)

        self.assertEqual(b.image.get_width(), 12)
        self.assertEqual(b.image.get_height(), 13)
        self.assertEqual(b.image.get_at((5, 5)), (0, 0, 255, 255))
        self.assertEqual(b.rect.centerx, 10)
        self.assertEqual(b.rect.centery, 20)
        self.assertEqual(b.destination_x, 40)
        self.assertEqual(b.destination_y, 60)
        self.assertEqual(b.frame_destroy_after, 10)
        self.assertEqual(b.frame_to_hit_Ballon, 2.5)
        self.assertEqual(b.step_x, 12)
        self.assertEqual(b.step_y, 16)
        self.assertEqual(mock_ballon_group_add.call_count, 1)

    @patch.object(pygame.sprite.Sprite, 'kill')
    @patch.multiple(bullet.Bullet, __abstractmethods__=set())
    def test_update_if_block(self, mock_sprite_kill):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1

        b = bullet.Bullet(start, destination, pop_power )
        b.rect.centerx = 50
        b.rect.centery = 60
        b.step_x = 5
        b.step_y = 6
        b.frame_destroy_after = 10

        b.update()
        self.assertEqual(b.rect.centerx, 55)
        self.assertEqual(b.rect.centery, 66)
        self.assertEqual(b.frame_destroy_after, 9)
        self.assertEqual(mock_sprite_kill.call_count, 0)

    @patch.object(pygame.sprite.Sprite, 'kill')
    @patch.multiple(bullet.Bullet, __abstractmethods__=set())
    def test_update_else_block(self, mock_sprite_kill):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1

        b = bullet.Bullet(start, destination, pop_power)
        b.rect.centerx = 50
        b.rect.centery = 60
        b.step_x = 5
        b.step_y = 6
        b.frame_destroy_after = 0

        b.update()
        self.assertEqual(b.rect.centerx, 50)
        self.assertEqual(b.rect.centery, 60)
        self.assertEqual(b.frame_destroy_after, 0)
        self.assertEqual(mock_sprite_kill.call_count, 1)



class TestStandardBullet(TestCase):

    @patch.object(pygame.sprite.Sprite, 'kill')
    def test_handle_balloon_collision(self, mock_sprite_kill):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1

        s = bullet.StandardBullet(start, destination, pop_power)
        s.handle_ballon_collision()

        self.assertEqual(mock_sprite_kill.call_count, 1)


class TestExplosionBullet(TestCase):
    @patch.object(pygame.sprite.Group, 'add')
    @patch.object(bullet, 'create_bullet')
    @patch.object(pygame.sprite.Sprite, 'kill')
    def test_handle_balloon_collision(self, mock_sprite_kill, mock_create_bullet, mock_sprite_group_add):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1

        s = bullet.ExplosionBullet(start, destination, pop_power)
        s.handle_ballon_collision(Mock(spec=pygame.sprite.Group))

        self.assertEqual(mock_sprite_group_add.call_count, 1)
        self.assertEqual(mock_create_bullet.call_count, 4)
        self.assertEqual(mock_sprite_kill.call_count, 1)


class TestTeleportationBullet(TestCase):
    @patch.object(pygame.sprite.Sprite, 'kill')
    def test_handle_balloon_collision(self, mock_sprite_kill):
        start = (10, 20)
        destination = (40, 60)
        pop_power = 1

        s = bullet.TeleportationBullet(start, destination, pop_power)
        s.handle_ballon_collision()

        self.assertEqual(mock_sprite_kill.call_count, 1)

class TestBulletModule(TestCase):
    def test_create_bullet_with_STANDARD_BULLET(self):
        start = (0, 0)
        destination = (10, 10)
        pop_power = 1

        s = bullet.create_bullet(bullet.STANDARD_BULLET, start, destination, pop_power)

        self.assertIsInstance(s, bullet.StandardBullet)

    def test_create_bullet_with_EXPLOSION_BULLET(self):
        start = (0, 0)
        destination = (10, 10)
        pop_power = 1

        s = bullet.create_bullet(bullet.EXPLOSION_BULLET, start, destination, pop_power)

        self.assertIsInstance(s, bullet.ExplosionBullet)

    def test_create_bullet_with_TELEPORTATION_BULLET(self):
        start = (0, 0)
        destination = (10, 10)
        pop_power = 1

        s = bullet.create_bullet(bullet.TELEPORTATION_BULLET, start, destination, pop_power)

        self.assertIsInstance(s, bullet.TeleportationBullet)

    def test_create_bullet_with_invalid_bullet(self):
        start = (0, 0)
        destination = (10, 10)
        pop_power = 1

        self.assertRaises(NotImplementedError, bullet.create_bullet, 'invalid bullet', start, destination, pop_power)

