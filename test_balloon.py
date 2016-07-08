import unittest
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

import balloon
import pygame
import bullet
import path
import bank


class TestBalloon(TestCase):
    def test_init_with_all_params(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p, 30, 40)

        self.assertEqual(b.image.get_width(), 50)
        self.assertEqual(b.image.get_height(), 60)
        self.assertEqual(b.image.get_at((10, 10)), (0, 0, 255, 255))
        self.assertEqual(b.path_index, 40)
        self.assertEqual(b.rect.centerx, 100)
        self.assertEqual(b.rect.centery, 70)
        self.assertEqual(b.path, p)
        self.assertEqual(b.bounty, 30)

    def test_init_with_defaults(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        self.assertEqual(b.image.get_width(), 50)
        self.assertEqual(b.image.get_height(), 60)
        self.assertEqual(b.image.get_at((10, 10)), (0, 0, 255, 255))
        self.assertEqual(b.path_index, 0)
        self.assertEqual(b.rect.centerx, 100)
        self.assertEqual(b.rect.centery, 30)
        self.assertEqual(b.path, p)
        self.assertEqual(b.bounty, 20)

    @patch.object(pygame.sprite, 'spritecollide')
    def test_update_with_no_collided_bullets(self, mock_spritecollide):
        mock_spritecollide.return_value = None
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        return_value = b.update('fake_bullet_sprites')

        self.assertIsNone(return_value)

    @patch.object(pygame.sprite, 'spritecollide')
    def test_update_with_StandardBullet_as_collided_bullets(self, mock_spritecollide):
        collided_bullets = Mock(spec=bullet.StandardBullet)
        collided_bullets.pop_power = Mock(spec=int)

        mock_spritecollide.return_value = [collided_bullets]

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        return_value = b.update('fake_bullet_sprites')

        self.assertIsInstance(return_value, int)


    @patch.object(pygame.sprite, 'spritecollide')
    def test_update_with_ExplosionBullet_as_collided_bullets(self, mock_spritecollide):
        collided_bullets = Mock(spec=bullet.ExplosionBullet)
        collided_bullets.pop_power = Mock(spec=int)
        mock_spritecollide.return_value = [collided_bullets]

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        return_value = b.update('fake_bullet_sprites')

        self.assertIsInstance(return_value, int)

    @patch.object(pygame.sprite, 'spritecollide')
    def test_update_with_TeleportationBullet_as_collided_bullets(self, mock_spritecollide):
        collided_bullets = Mock(spec=bullet.TeleportationBullet)
        mock_spritecollide.return_value = [collided_bullets]

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        return_value = b.update('fake_bullet_sprites')

        self.assertFalse(return_value)

    @patch.object(pygame.sprite, 'spritecollide')
    def test_update_with_invalid_type_as_collided_bullets(self, mock_spritecollide):
        collided_bullets = Mock(spec=int)
        mock_spritecollide.return_value = [collided_bullets]

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        self.assertRaises(NotImplementedError, b.update, 'fake_bullet_sprites')

    def test_move_with_valid_path_index(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.path_index = 10

        b.move()
        self.assertEqual(b.rect.centerx, 100)
        self.assertEqual(b.rect.centery, 40)
        self.assertEqual(b.path_index, 11)

    def test_move_with_out_of_range_path_index(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)

        b.path_index = 329
        self.assertRaises(NotImplementedError, b.move)

        b.path_index = 500
        self.assertRaises(NotImplementedError, b.move)

    def test_teleport_with_larger_default_back_track(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.path_index = 10
        b.teleport()

        self.assertEqual(b.path_index, 0)

    def test_teleport_with_smaller_default_back_track(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.path_index = 50
        b.teleport()

        self.assertEqual(b.path_index, 30)

    def test_teleport_with_larger_custom_back_track(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.path_index = 50
        b.teleport(70)

        self.assertEqual(b.path_index, 0)

    def test_teleport_with_smaller_custom_back_track(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.path_index = 50
        b.teleport(40)

        self.assertEqual(b.path_index, 10)


class TestBalloonL1(TestCase):
    def test_peel_layer(self):
        p = [(100, y) for y in range(30, 360)]
        b1 = balloon.BalloonL1((0, 0, 255), (50, 60), p)

        return_value = b1.peel_layer()
        self.assertIsNone(return_value)


class TestBalloonL2(TestCase):
    def test_peel_layer(self):
        p = [(100, y) for y in range(30, 360)]
        b2 = balloon.BalloonL2((0, 0, 255), (50, 60), p)

        return_value = b2.peel_layer()
        self.assertIsInstance(return_value, balloon.BalloonL1)


class TestBalloonL3(TestCase):
    def test_peel_layer(self):
        p = [(100, y) for y in range(30, 360)]
        b3 = balloon.BalloonL3((0, 0, 255), (50, 60), p)

        return_value = b3.peel_layer()
        self.assertIsInstance(return_value, balloon.BalloonL2)


class TestBalloonL4(TestCase):
    def test_peel_layer(self):
        p = [(100, y) for y in range(30, 360)]
        b4 = balloon.BalloonL4((0, 0, 255), (50, 60), p)

        return_value = b4.peel_layer()
        self.assertIsInstance(return_value, balloon.BalloonL3)


class TestBalloonL5(TestCase):
    def test_peel_layer(self):
        p = [(100, y) for y in range(30, 360)]
        b5 = balloon.BalloonL5((0, 0, 255), (50, 60), p)

        return_value = b5.peel_layer()
        self.assertIsInstance(return_value, balloon.BalloonL4)


class TestBalloonContext(TestCase):
    def test_init(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        balloon_context = balloon.BalloonContext(b)
        self.assertEqual(balloon_context.current_ballon, b)

    @patch.object(balloon.Balloon, 'update')
    @patch.object(balloon.BalloonContext, 'handle_pop')
    def test_update_with_true_is_handle_pop(self, mock_handle_pop, mock_update):
        mock_update.return_value = True

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        balloon_context = balloon.BalloonContext(b)

        balloon_context.update('fake_bullet_sprites')
        self.assertEqual(mock_handle_pop.call_count, 1)

    @patch.object(balloon.Balloon, 'update')
    @patch.object(balloon.BalloonContext, 'handle_pop')
    def test_update_with_false_is_handle_pop(self, mock_handle_pop, mock_update):
        mock_update.return_value = False

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        balloon_context = balloon.BalloonContext(b)

        balloon_context.update('fake_bullet_sprites')
        self.assertEqual(mock_handle_pop.call_count, 0)

    @patch.object(balloon.Balloon, 'update')
    @patch.object(balloon.BalloonContext, 'handle_pop')
    def test_update_with_none_is_handle_pop(self, mock_handle_pop, mock_update):
        mock_update.return_value = None

        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        balloon_context = balloon.BalloonContext(b)

        balloon_context.update('fake_bullet_sprites')
        self.assertEqual(mock_handle_pop.call_count, 0)

    @patch.object(bank, 'deposit')
    @patch.object(balloon.BalloonL5, 'peel_layer')
    @patch.object(pygame.sprite.Sprite, 'kill')
    def test_handle_pop_with_None_current_ballon(self, mock_kill, mock_peel_layer, mock_deposit):
        mock_peel_layer.return_value = None

        p = [(100, y) for y in range(30, 360)]
        bL5 = balloon.BalloonL5((0, 0, 255), (50, 60), p)
        balloon_context = balloon.BalloonContext(bL5)
        original_bounty = balloon_context.current_ballon.bounty
        balloon_context.handle_pop()

        self.assertEqual(mock_kill.call_count, 0)
        self.assertEqual(mock_deposit.call_count, 1)
        mock_deposit.assert_called_with(original_bounty)

    @patch.object(bank, 'deposit')
    @patch.object(balloon.BalloonL5, 'peel_layer')
    @patch.object(pygame.sprite.Sprite, 'kill')
    def test_handle_pop_with_None_current_ballon(self, mock_kill, mock_peel_layer, mock_deposit):
        mock_peel_layer.return_value = balloon.create_balloon(balloon.BALLOON_L4, path.Path())

        p = [(100, y) for y in range(30, 360)]
        bL5 = balloon.BalloonL5((0, 0, 255), (50, 60), p)
        balloon_context = balloon.BalloonContext(bL5)
        original_bounty = balloon_context.current_ballon.bounty
        balloon_context.handle_pop(1)

        self.assertEqual(mock_kill.call_count, 0)
        self.assertEqual(mock_deposit.call_count, 1)
        mock_deposit.assert_called_with(original_bounty)


    def test_get_centerX(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.rect.centerx = 120
        balloon_context = balloon.BalloonContext(b)

        return_value = balloon_context.get_centerX()

        self.assertEqual(return_value, 120)

    def test_get_centerX(self):
        p = [(100, y) for y in range(30, 360)]
        b = balloon.Balloon((0, 0, 255), (50, 60), p)
        b.rect.centery = 120
        balloon_context = balloon.BalloonContext(b)

        return_value = balloon_context.get_centerY()

        self.assertEqual(return_value, 120)


class TestBalloonModule(TestCase):
    def test_create_balloon_BALLOON_L1(self):
        return_value = balloon.create_balloon(balloon.BALLOON_L1, path.Path())
        self.assertIsInstance(return_value, balloon.BalloonL1)

    def test_create_balloon_BALLOON_L2(self):
        return_value = balloon.create_balloon(balloon.BALLOON_L2, path.Path())
        self.assertIsInstance(return_value, balloon.BalloonL2)

    def test_create_balloon_BALLOON_L3(self):
        return_value = balloon.create_balloon(balloon.BALLOON_L3, path.Path())
        self.assertIsInstance(return_value, balloon.BalloonL3)

    def test_create_balloon_BALLOON_L4(self):
        return_value = balloon.create_balloon(balloon.BALLOON_L4, path.Path())
        self.assertIsInstance(return_value, balloon.BalloonL4)

    def test_create_balloon_BALLOON_L5(self):
        return_value = balloon.create_balloon(balloon.BALLOON_L5, path.Path())
        self.assertIsInstance(return_value, balloon.BalloonL5)

    def test_create_balloon_exception(self):
        self.assertRaises(NotImplementedError, balloon.create_balloon, 'Invalid type', path.Path())

    def test_create_balloon_context(self):
        return_value = balloon.create_balloon_context(balloon.BALLOON_L3, path.Path())
        self.assertIsInstance(return_value, balloon.BalloonContext)


