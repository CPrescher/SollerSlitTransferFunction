from calc_dispersion_angle_map import calculate_dispersion_angle_matrix, create_beautiful_plot
import matplotlib.pyplot as plt

#
# lets first create it for several thicknesses with normal geometry:

r1 = 62 # defines the radius to the inner slit set
r2 = 210 # defines the radius to the outer slit set
w1 = 0.05 # the width of one of the inner slits
w2 = 0.2 # the width of one of the outer slits
b1 = 8 # length of the inner slits
b2 = 6 # length of the outer slits


two_theta_array, distance_array, phi_array = calculate_dispersion_angle_matrix(r1, r2, w1, w2, b1, b2)
create_beautiful_plot(two_theta_array, distance_array, phi_array, example_thickness=0.04)
plt.savefig('output/dispersion_map_standard_30micron.png', dpi=150)

create_beautiful_plot(two_theta_array, distance_array, phi_array, example_thickness=0.100)
plt.savefig('output/dispersion_map_standard_100micron.png', dpi=150)


# # now with smaller outer slit size
two_theta_array, distance_array, phi_array = calculate_dispersion_angle_matrix(r1, r2, w1, 0.1, b1, b2)
figure, _, _, ax3, _ =  create_beautiful_plot(two_theta_array, distance_array, phi_array, example_thickness=0.040)
plt.figure(figure.number)
plt.sca(ax3)
plt.ylim((0.999, 1.001))
plt.savefig('output/dispersion_map_modified_30micron.png', dpi=150)

create_beautiful_plot(two_theta_array, distance_array, phi_array, example_thickness=0.100)
plt.savefig('output/dispersion_map_modified_100micron.png', dpi=150)

plt.show()