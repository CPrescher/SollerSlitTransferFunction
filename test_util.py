# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'


import unittest

import numpy as np

from util import calculate_angles


class TestUtilLibrary(unittest.TestCase):
    def test_calculate_angles_for_single_values(self):
        p1 = [0, 1]
        p2 = [1, 0]
        c = [0, 0]

        angle = calculate_angles(p1, p2, c)
        self.assertAlmostEqual(angle, np.pi/2)

    def test_calculat_angles_for_multiple_centers(self):
        p1 = [0, 1]
        p2 = [1, 0]
        c = np.linspace(-0.5, 0.5)

        angles = calculate_angles(p1, p2, c)
        self.assertAlmostEqual(np.sum(angles), np.pi/2*len(c))


