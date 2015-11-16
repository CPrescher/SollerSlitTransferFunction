# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'




############################################################################################################
#### This script calculates the dispersion angle along a sample thickness for a multichannel collimator ####
#### geometry defined in the parameters file. It is called simple because it approximates each slit
#### with a point, thus, the slit length does not matter anymore.
############################################################################################################

import os
os.environ['QT_GRAPHICSSYSTEM']='native'
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


from util import *
from parameters import r1, r2, w1, w2, b1, b2, example_thickness

two_theta_array = np.linspace(1, 40, 500) / 180. * np.pi
p_x = np.linspace(-0.2, 0.2, 500)
p_y = np.zeros(p_x.shape)
p = np.array([p_x, p_y])
phi_array = []
for two_theta in two_theta_array:
    # calculate fix points for the ther outer parts of the slits
    s1, s2 = calculate_rectangular_side_points(r1+b1*0.5, two_theta, w1)
    q1, q2 = calculate_rectangular_side_points(r2+b2*0.5, two_theta, w2)


    # calculate the angles to the outer points of the slits
    phi1 = calculate_angles(s1, s2, p)
    phi2 = calculate_angles(q1, q2, p)

    # take the smallest angle for each point
    phi = np.where(phi1 < phi2, phi2, phi1)


    intercept_s1_q1 = calculate_x_axis_intercept(s1, q1)
    intercept_s1_q2 = calculate_x_axis_intercept(s1, q2)
    intercept_s2_q1 = calculate_x_axis_intercept(s2, q1)
    intercept_s2_q2 = calculate_x_axis_intercept(s2, q2)

    phi[p[0] < intercept_s1_q2] = 0
    phi[p[0] > intercept_s2_q1] = 0

    intermediate_region_ind = np.logical_and(p_x > intercept_s1_q2, p_x < intercept_s1_q1)
    intermediate_region_ind = np.logical_and(intermediate_region_ind, p_x<0)
    points_in_intermediate_region = p[:, intermediate_region_ind]
    phi[intermediate_region_ind] = calculate_angles(s1, q2, points_in_intermediate_region)

    intermediate_region_ind = np.logical_and(p_x < intercept_s2_q1, p_x > intercept_s2_q2)
    intermediate_region_ind = np.logical_and(intermediate_region_ind, p_x>0)
    points_in_intermediate_region = p[:, intermediate_region_ind]
    phi[intermediate_region_ind] = calculate_angles(s2, q1, points_in_intermediate_region)

    phi_array.append(phi)

X, Y = np.meshgrid(two_theta_array / np.pi * 180, p[0])
phi_array = np.array(phi_array).transpose()

line_ind = 350

plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
ax1 = plt.subplot(gs[0])
plt.title("Dispersion angle through two slits")
plt.contourf(X, Y, phi_array, 200, fontsize=14, cmap=plt.cm.get_cmap("jet"))
con = plt.contour(X, Y, phi_array, 6, colors='k')
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
plt.savefig("dispersion_angle_two_slits_simple.png", dpi=300)
plt.show()
