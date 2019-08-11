import math
import numpy as np
import matplotlib.pyplot as plt
import os

# this messes wiht tkninter for some reason
# matplotlib.use('Qt5Agg')

SIGFIGS = 3


class MohrsFindPrincipal:

    def __init__(self, sigma_a, sigma_b, tau, temp_dir, angle, units, show_principal=True):
        self.sigma_a = sigma_a
        self.sigma_b = sigma_b
        self.tau = tau
        self.units = units
        self.angle = angle
        self.show_principal = show_principal
        self.rad = 0
        self.center_x = 0
        self.angles = []
        self.temp_dir = temp_dir

    def principal_stress(self):
        # finds center and radius
        # radius is also pure shear max
        # center_x is also the sigma average
        self.center_x = (self.sigma_a + self.sigma_b) / 2
        self.rad = np.sqrt((self.sigma_a - self.center_x) ** 2 + self.tau ** 2)

        # finds principal stresses
        p1 = self.center_x + self.rad
        p2 = self.center_x - self.rad

        # finds angles for principal stresses and pure shear
        if self.sigma_a - self.center_x == 0:
            alpha = 90
        else:
            alpha = (np.arctan(self.tau / (self.sigma_a - self.center_x)) * 180) / np.pi

        # this finds angles and puts them all in a list of angles
        theta_p1 = alpha / 2
        theta_p2 = theta_p1 + 90
        theta_pure_shear_1 = (-90 + alpha) / 2
        theta_pure_shear_2 = (theta_pure_shear_1 + 90)
        self.angles = [alpha, theta_p1, theta_p2, theta_pure_shear_1, theta_pure_shear_2]
        if self.angle != 0:
            beta = (((-2 * self.angle) + alpha) * np.pi) / 180
            max_inplane_x = self.center_x + (self.rad * np.cos(beta))
            max_inplane_y = self.center_x - (self.rad * np.cos(beta))
            plane_shear = -self.rad * np.sin(beta)
            self.angles.append((beta * 180) / np.pi)
            return [self.center_x, self.rad, p1, p2, theta_p1, theta_p2, theta_pure_shear_1, theta_pure_shear_2,
                    max_inplane_x, max_inplane_y, plane_shear]
        else:
            return [self.center_x, self.rad, p1, p2, theta_p1, theta_p2, theta_pure_shear_1, theta_pure_shear_2]

    def visualize(self):
        # this function creates a mohrs circle with the parameters passed to the class
        # it then creates all of the labels and used matplotlib and pillow to save the created graph as a png
        # this saves to a temp dir
        principal = self.principal_stress()

        # this configures the correct plot sizing
        plt.figure(figsize=(10, 5))

        # configurable options for what displays depending on whether an additional plane angle is input
        if self.angle != 0 and self.show_principal is True:
            x_values = [principal[0], self.sigma_a, self.sigma_b, principal[2], principal[3], self.center_x,
                        self.center_x, principal[8], principal[9], principal[8], principal[9]]
            y_values = [0, self.tau, -self.tau, 0, 0, self.rad, -self.rad, -principal[10],
                        principal[10], -principal[10], principal[10]]
            points_label = ['Center', 'Stress in x', 'Stress in y', 'Principal stress x', 'Principal stress y',
                            'Max shear', 'Min shear', 'In-plane max stress x', 'In-plane max stress y',
                            'In-plane max shear stress', 'In-plane min shear stress']
        elif self.angle != 0 and self.show_principal is False:
            x_values = [principal[0], self.sigma_a, self.sigma_b, self.center_x, self.center_x,
                        principal[8], principal[9], principal[8], principal[9]]
            y_values = [0, self.tau, -self.tau, self.rad, -self.rad, -principal[10],
                        principal[10], -principal[10], principal[10]]
            points_label = ['Center', 'Stress in x', 'Stress in y', 'Max shear', 'Min shear', 'In-plane max stress x',
                            'In-plane max stress y', 'In-plane max shear stress',
                            'In-plane min shear stress']
        elif self.angle == 0 and self.show_principal is False:
            x_values = [principal[0], self.sigma_a, self.sigma_b, self.center_x, self.center_x]
            y_values = [0, self.tau, -self.tau, self.rad, -self.rad]
            points_label = ['Center', 'Stress in x', 'Stress in y', 'Max shear', 'Min shear']
        else:
            x_values = [principal[0], self.sigma_a, self.sigma_b, principal[2], principal[3], self.center_x,
                        self.center_x]
            y_values = [0, self.tau, -self.tau, 0, 0, self.rad, -self.rad]
            points_label = ['Center', 'Stress in x', 'Stress in y', 'Principal stress x', 'Principal stress 2y',
                            'Max shear', 'Min shear']

        # labels the points for the legend and gives each a value
        points_label[0] = (str(points_label[0]) + '= ' + str(round_sigfigs((x_values[0]), SIGFIGS)) +
                           str(round_sigfigs((y_values[0]), SIGFIGS)) + self.units)
        if self.show_principal is True:
            for i in range(1, 5):
                points_label[i] = (str(points_label[i]) + '= '
                                   + str(round_sigfigs((x_values[i]), SIGFIGS))
                                   + self.units)

            for i in range(5, 7):
                points_label[i] = (str(points_label[i]) + '= '
                                   + str(round_sigfigs((y_values[i]), SIGFIGS))
                                   + self.units)

            if self.angle != 0:
                for i in range(7, 9):
                    points_label[i] = (str(points_label[i]) + '= ' +
                                       str(round_sigfigs((x_values[i]), SIGFIGS))
                                       + self.units)
                for i in range(9, 11):
                    points_label[i] = (str(points_label[i]) + '= ' +
                                       str(round_sigfigs((y_values[i]), SIGFIGS))
                                       + self.units)

        if self.show_principal is False:
            for i in range(1, 3):
                points_label[i] = (str(points_label[i]) + '= '
                                   + str(round_sigfigs((x_values[i]), SIGFIGS))
                                   + self.units)

            for i in range(3, 5):
                points_label[i] = (str(points_label[i]) + '= '
                                   + str(round_sigfigs((y_values[i]), SIGFIGS))
                                   + self.units)

            if self.angle != 0:
                for i in range(5, 7):
                    points_label[i] = (str(points_label[i]) + '= ' +
                                       str(round_sigfigs((x_values[i]), SIGFIGS))
                                       + self.units)
                for i in range(7, 9):
                    points_label[i] = (str(points_label[i]) + '= ' +
                                       str(round_sigfigs((y_values[i]), SIGFIGS))
                                       + self.units)



        colors = ['black', 'darkred', 'red', 'moccasin', 'orange', 'lightgreen',
                  'darkgreen', 'purple', 'mediumorchid', 'lightseagreen', 'gold']
        # prints points
        for i in range(len(x_values)):
            plt.scatter(x_values[i], y_values[i], marker='o', color=colors[i], label=points_label[i])
        # prints lines between points
        for i in range(1, len(x_values), 2):
            plt.plot([x_values[i], x_values[i+1]], [y_values[i], y_values[i+1]], color=colors[i], linewidth=1)

        # plot alpha
        n = 64
        t = np.linspace(0, math.radians(self.angles[0]), n + 1)
        x = (self.rad / 3) * np.cos(t) + self.center_x
        y = (self.rad / 3) * np.sin(t)
        plt.plot(x, y, label='alpha = ' + str(round(self.angles[0])) + ' degrees', color='blue')

        # plot phi
        n = 64
        t = np.linspace(math.radians(self.angles[0]), math.radians(90), n + 1)
        x = (self.rad / 2) * np.cos(t) + self.center_x
        y = (self.rad / 2) * np.sin(t)
        plt.plot(x, y, label='phi = ' + str(round(90 - self.angles[0])) + ' degrees', color='orange')

        # plot beta
        if self.angle != 0:
            n = 64
            t = np.linspace(math.radians(self.angles[0]), math.radians(self.angles[5]), n + 1)
            x = (self.rad / 2.5) * np.cos(t) + self.center_x
            y = (self.rad / 2.5) * np.sin(t)
            plt.plot(x, y, label='beta = ' + str(round(self.angles[5] - self.angles[0])) + ' degrees', color='green')

        # displays circle
        n = 64
        t = np.linspace(0, 2 * np.pi, n + 1)
        x = self.rad * np.cos(t) + self.center_x
        y = self.rad * np.sin(t)
        plt.plot(x, y, color='black')

        # plots axes and shrinks it to put a legend outside of graph
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
        legend_x = 1
        legend_y = 0.5
        plt.legend(["blue", "green"], loc='center left', bbox_to_anchor=(legend_x, legend_y))
        plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))

        # plot options
        plt.title('Mohrs Circle')
        plt.gca().invert_yaxis()
        plt.xlabel('Normal Stress')
        plt.ylabel('Shear Stress')
        plt.axis('equal')
        plt.grid()

        # saves as png
        path = os.path.join(self.temp_dir, 'mohrs.png')
        print(path)
        plt.savefig(path)


# this method returns any number of sig figs for a given number
def round_sigfigs(num, sig_figs):

    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0

# this code will test the mohrs circle and save a picture of it into the temp dir that it creates

# circle = Mohrs_Find_Principal(STRESS_IN_X, STRESS_IN_Y, SHEAR_XY, ANGLE, UNITS, SHOW_PRINCIPAL)
# circle.visualize()
