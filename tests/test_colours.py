import unittest
from unittest.mock import Mock
from unittest.mock import patch

import colours


class TestColoursModule(unittest.TestCase):
    def test_red(self):
        self.assertEqual(colours.RED, (255, 0, 0, 255))

    def test_orange(self):
        self.assertEqual(colours.ORANGE, (255, 165, 0, 255))

    def test_yellow(self):
        self.assertEqual(colours.YELLOW, (255, 255, 0, 255))

    def test_green(self):
        self.assertEqual(colours.GREEN, (0, 255, 0, 255))

    def test_blue(self):
        self.assertEqual(colours.BLUE, (0, 0, 255, 255))

    def test_cyan(self):
        self.assertEqual(colours.CYAN, (0, 255, 255, 255))

    def test_purple(self):
        self.assertEqual(colours.PURPLE, (255, 0, 255, 255))

    def test_black(self):
        self.assertEqual(colours.BLACK, (0, 0, 0, 255))

    def test_white(self):
        self.assertEqual(colours.WHITE, (255, 255, 255, 255))

    def test_gray(self):
        self.assertEqual(colours.GRAY, (128, 128, 128, 255))

    def test_brown(self):
        self.assertEqual(colours.BROWN, (165, 42, 42, 255))
