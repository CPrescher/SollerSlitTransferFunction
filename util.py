# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import numpy as np

def vector_length(vec):
    return np.sqrt(np.sum(vec**2))

def calculate_angles(point1, point2, p):
    """
    calculates the angle between vectors going from the two points (point1, point2) to a central point p using
    the dot product.
    """
    return np.arccos(((point1[0]-p[0])*(point2[0]-p[0])+(point1[1]-p[1])*(point2[1]-p[1]))/
                     (np.sqrt((point1[0]-p[0])**2+(point1[1]-p[1])**2)*np.sqrt((point2[0]-p[0])**2+(point2[1]-p[1])**2)))


def calculate_x_axis_intercept(p1, p2):
    """
    obtains the x-axis intercept of a line defined by two points.
    """
    m = p2 - p1
    l = -p2[1]/m[1]
    return l*m[0]+p2[0]

def calculate_y_axis_intercept(p1, p2):
    """
    obtains the y-axis intercept of a line defined by two points.
    """
    m = (p2[1]-p1[1])/(p2[0]-p1[0])
    return m*(-p2[0])+p2[1]
