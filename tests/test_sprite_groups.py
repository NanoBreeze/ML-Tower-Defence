import unittest
from unittest.mock import Mock
from unittest.mock import patch

import icon
import colours
import tower
import sprite_groups
import pygame

class TestSpriteGroupsModule(unittest.TestCase):

    def test_instance_of_bullet_sprites(self):
        self.assertIsInstance(sprite_groups.bullet_sprites, pygame.sprite.Group)

    def test_instance_of_tower_sprites(self):
        self.assertIsInstance(sprite_groups.tower_sprites, pygame.sprite.Group)

    def test_instance_of_balloon_sprites(self):
        self.assertIsInstance(sprite_groups.balloon_sprites, sprite_groups.BalloonGroup)

    def test_instance_of_tower_icon_sprites(self):
        self.assertIsInstance(sprite_groups.tower_icon_sprites, pygame.sprite.Group)

    def test_instance_of_selected_tower_icon_sprite(self):
        self.assertIsInstance(sprite_groups.selected_tower_icon_sprite, pygame.sprite.GroupSingle)
