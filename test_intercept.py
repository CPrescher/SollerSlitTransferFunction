# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')


from util import *
from parameters import r1, r2, w1, w2, b1, b2, example_thickness

two_theta_array = np.linspace(10, 40, 500) / 180. * np.pi
p_x = np.linspace(-0.2, 0.2, 500)
p_y = np.zeros(p_x.shape)
p = np.array([p_x, p_y])
phi_array = []

intercepts_s1_1_q1_2 = []
intercepts_s1_1_q2_2 = []

intercepts_s1_1_q1_1 = []
intercepts_q1_1_q2_1 = []

for two_theta in two_theta_array:
    # calculate fix points for the ther outer parts of the slits
    q1_1, q1_2 = calculate_rectangular_side_points(r1+b1, two_theta, w1)
    q2_1, q2_2 = calculate_rectangular_side_points(r2+b2, two_theta, w2)

    # calculate fix points for the inner parts of the slits
    s1_1, s1_2 = calculate_rectangular_side_points(r1, two_theta, w1)
    s2_1, s2_2 = calculate_rectangular_side_points(r2, two_theta, w2)


    #intercepts for left angle
    intercept_s1_1_q1_2 = calculate_x_axis_intercept(s1_1, q1_2)
    intercept_s1_1_q2_2 = calculate_x_axis_intercept(s1_1, q2_2)

    intercepts_s1_1_q1_2.append(intercept_s1_1_q1_2)
    intercepts_s1_1_q2_2.append(intercept_s1_1_q2_2)

    intercept_s1_1_q1_1 = calculate_x_axis_intercept(s1_1, q1_1)
    intercept_q1_1_q2_1 = calculate_x_axis_intercept(q1_1, q2_1)

    intercepts_s1_1_q1_1.append(intercept_s1_1_q1_1)
    intercepts_q1_1_q2_1.append(intercept_q1_1_q2_1)


two_theta_array_degree = two_theta_array * 180 / np.pi

# plt.plot(two_theta_array_degree, intercepts_s1_1_q1_2, label = 'S1_1_Q1_2')
plt.plot(two_theta_array_degree, intercepts_s1_1_q2_2, label = 'S1_1_Q2_2')
plt.legend()

plt.figure()
plt.plot(two_theta_array_degree, intercepts_s1_1_q1_1, label = 'S1_1_Q1_1')
plt.plot(two_theta_array_degree, intercepts_q1_1_q2_1, label = 'Q1_1_Q2_1')
plt.legend()

plt.show()