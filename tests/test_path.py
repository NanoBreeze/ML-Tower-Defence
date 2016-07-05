import unittest
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

import path

class TestPath(TestCase):
    def test_init(self):
        p = path.Path()

        points = [(100, y) for y in range(30, 360)]
        self.assertEqual(p.points, points)

    def test_length(self):
        p = path.Path()
        length = len(p)

        self.assertEqual(length, 330)

    def test_with_valid_get_item(self):
        p = path.Path()
        return_value = p[5]

        self.assertEqual(return_value, (100, 35))

    def test_with_out_of_range_get_item(self):
        p = path.Path()

        self.assertRaises(IndexError, p.__getitem__, 10000)

    def test_with_negative_item_get_item(self):
        p = path.Path()
        return_value = p[-5]

        self.assertEqual(return_value, (100, 355))

    def test_slicing_get_item(self):
        p = path.Path()
        return_value = p[2:5]

        self.assertEqual(return_value, [(100, 32), (100, 33), (100, 34) ])