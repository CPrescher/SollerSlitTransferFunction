# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')


from util import *
from parameters import r1, r2, w1, w2, b1, b2, example_thickness

two_theta_array = np.linspace(2, 50, 500) / 180. * np.pi
p_x = np.linspace(-0.2, 0.2, 500)
p_y = np.zeros(p_x.shape)
p = np.array([p_x, p_y])
phi_array = []
for two_theta in two_theta_array:
    # calculate fix points for the ther outer parts of the slits
    q1_1 = np.array([(r1 + b1) * np.cos(two_theta) - 0.5 * w1 * np.sin(two_theta),
                     (r1 + b1) * np.sin(two_theta) + 0.5 * w1 * np.cos(two_theta)])

    q1_2 = np.array([(r1 + b1) * np.cos(two_theta) + 0.5 * w1 * np.sin(two_theta),
                     (r1 + b1) * np.sin(two_theta) - 0.5 * w1 * np.cos(two_theta)])

    q2_1 = np.array([(r2 + b2) * np.cos(two_theta) - 0.5 * w2 * np.sin(two_theta),
                     (r2 + b2) * np.sin(two_theta) + 0.5 * w2 * np.cos(two_theta)])

    q2_2 = np.array([(r2 + b2) * np.cos(two_theta) + 0.5 * w2 * np.sin(two_theta),
                     (r2 + b2) * np.sin(two_theta) - 0.5 * w2 * np.cos(two_theta)])

    # calculate fix points for the inner parts of the slits
    s1_1 = np.array([r1 * np.cos(two_theta) - 0.5 * w1 * np.sin(two_theta),
                     r1 * np.sin(two_theta) + 0.5 * w1 * np.cos(two_theta)])

    s1_2 = np.array([r1 * np.cos(two_theta) + 0.5 * w1 * np.sin(two_theta),
                     r1 * np.sin(two_theta) - 0.5 * w1 * np.cos(two_theta)])

    s2_1 = np.array([r2 * np.cos(two_theta) - 0.5 * w2 * np.sin(two_theta),
                     r2 * np.sin(two_theta) + 0.5 * w2 * np.cos(two_theta)])

    s2_2 = np.array([r2 * np.cos(two_theta) + 0.5 * w2 * np.sin(two_theta),
                     r2 * np.sin(two_theta) - 0.5 * w2 * np.cos(two_theta)])

    # calculate the angles to the outer points of the slits
    phi1 = calculate_angles(q1_1, q1_2, p)
    phi2 = calculate_angles(q2_1, q2_2, p)
    phi3 = calculate_angles(q2_1, q1_2, p)
    phi4 = calculate_angles(q1_1, q2_2, p)

    # take the smallest angle for each point
    phi = np.where(phi1 < phi2, phi1, phi2)
    phi = np.where(phi3 < phi, phi3, phi)
    phi = np.where(phi4 < phi, phi4, phi)

    #####################
    # correcting for positive side:
    intercept_s1_2_q1_1 = calculate_x_axis_intercept(s1_2, q1_1)
    intercept_s1_2_q1_2 = calculate_x_axis_intercept(s1_2, q1_2)

    intermediate_region_ind = np.logical_and(p_x > intercept_s1_2_q1_2, p_x < intercept_s1_2_q1_1)
    points_in_intermediate_region = np.array([p[0][intermediate_region_ind], p[1][intermediate_region_ind]])

    if np.sum(intermediate_region_ind):
        phi1 = calculate_angles(s1_2, q1_1, points_in_intermediate_region)
        phi2 = calculate_angles(s1_2, q2_1, points_in_intermediate_region)
        phi3 = calculate_angles(s2_2, q2_1, points_in_intermediate_region)
        phi[intermediate_region_ind] = np.where(phi1 < phi2, phi1, phi2)
        phi[intermediate_region_ind] = np.where(phi[intermediate_region_ind] < phi3, phi[intermediate_region_ind], phi3)

    # cut the angle
    intercept_s1_2_q1_1 = calculate_x_axis_intercept(s1_2, q1_1)
    phi[p[0] > intercept_s1_2_q1_1] = 0

    intercept_s1_2_q2_1 = calculate_x_axis_intercept(s1_2, q2_1)
    phi[p[0] > intercept_s1_2_q2_1] = 0

    ########################
    # correcting for negative side:
    intercept_s1_1_q1_2 = calculate_x_axis_intercept(s1_1, q1_2)
    intercept_s1_1_q1_1 = calculate_x_axis_intercept(s1_1, q1_1)

    intermediate_region_ind = np.logical_and(p_x < intercept_s1_1_q1_1, p_x > intercept_s1_1_q1_2)
    points_in_intermediate_region = np.array([p[0][intermediate_region_ind], p[1][intermediate_region_ind]])

    if np.sum(intermediate_region_ind):
        phi1 = calculate_angles(s1_1, q1_2, points_in_intermediate_region)
        phi2 = calculate_angles(s1_1, q2_2, points_in_intermediate_region)
        phi3 = calculate_angles(s2_1, q2_2, points_in_intermediate_region)
        phi[intermediate_region_ind] = np.where(phi1 < phi2, phi1, phi2)
        phi[intermediate_region_ind] = np.where(phi[intermediate_region_ind] < phi3, phi[intermediate_region_ind], phi3)

    # cutting the angles
    intercept_s1_1_q1_2 = calculate_x_axis_intercept(s1_1, q1_2)
    phi[p[0] < intercept_s1_1_q1_2] = 0

    intercept_s1_1_q2_2 = calculate_x_axis_intercept(s1_1, q2_2)
    phi[p[0] < intercept_s1_1_q2_2] = 0

    phi_array.append(phi)

X, Y = np.meshgrid(two_theta_array / np.pi * 180, p[0])
phi_array = np.array(phi_array).transpose()

line_ind = 350
plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
ax1 = plt.subplot(gs[0])
plt.title("Dispersion angle through two slits")
plt.contourf(X, Y, phi_array, 200, fontsize=14, cmap=plt.cm.get_cmap("jet"))
con = plt.contour(X, Y, phi_array, 8, colors='k')
plt.clabel(con, fmt='%3.1e', colors='k', fontsize=12)
plt.xlabel("$2\\theta$ $(\degree)$", fontsize=14)
plt.ylabel("x $(mm)$", fontsize=14)
# plotting the example thickness lines
x = X[0, :]
y = np.array([example_thickness / 2.0] * len(x))
plt.plot(x, y, 'k--')
plt.plot(x, -y, 'k--')

# plotting the intersection line for the right plot
plt.axvline(x[line_ind], color='w', ls='--')

ax2 = plt.subplot(gs[1])
phi = phi_array[:, line_ind] * 1e4
plt.plot(phi, p[0])
plt.ylim(p[0, 0], p[0, -1])
plt.xlabel("Dispersion angle $(\phi$ x $1e-4)$")
# example thickness lines:
x = phi
y = np.array([example_thickness / 2.0] * len(x))
plt.plot(x, y, 'k--')
plt.plot(x, -y, 'k--')

plt.tight_layout()
plt.show()