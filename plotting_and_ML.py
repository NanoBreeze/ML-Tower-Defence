"""Contains algo for machine learning and plotting tower positions"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import logging.config
import threading
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from sklearn.neighbors import KNeighborsClassifier

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

# the plot is a x, y z plot representing the position of towers and their pop values, where x is x position
# y is y position, and z is the pop count

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

x_pos = [0]
y_pos = [0]
z_pos = [0]  # zpos represents the count values, always starts at zero

dx = [0]
dy = [0]
dz = [0]  # this would be the height


# binary_semaphore = threading.Semaphore(value=1)  # since it is inconsistent to read and push to buffer


# def update_plot_with_pop_count(x, y, pop_count):
#     """Updates the bar at positions x and y with a new dz value equal to pop_count"""
#     logger.info('inside update pop_count')
#     # find corresponding index of x and y from the x_pos and y_pos. THen change the dz index to pop_count
#     matching_x_pos_indices = [i for i, x_value in enumerate(x_pos) if x_value == x]
#     matching_y_pos_indices = [i for i, y_value in enumerate(y_pos) if y_value == y]
#
#     logger.debug('x is: ' + str(matching_x_pos_indices))
#     logger.debug('y is: ' + str(matching_y_pos_indices))
#
#     z_index = set(matching_x_pos_indices).intersection(matching_y_pos_indices).pop()  # we want the only elemnent in this set
#
#     logger.info('z_index is: ' + str(z_index))
#     logger.info('pop_count is: ' + str(pop_count))
#
#     with binary_semaphore:
#         dz[z_index] = pop_count


def set_up_values(tower_stats_dict):
    """
    :param tower_stats_dict: a default dict of TowerStat. Corresponds to serverstats.tower_stats
    Sets up the x values (a list of all tower's x position), y values (a list of all tower's y position), and z values(number of pops by each tower)
    """

    logger.debug('inside setupvalues. tHe length of the dict is {}'.format(len(tower_stats_dict)))

    global x_pos
    global y_pos
    global z_pos
    global dx
    global dy
    global dz

    # reset all lists (this is an efficient way of doing it)
    x_pos = [0]
    y_pos = [0]
    z_pos = [0]
    dx = [0]
    dy = [0]
    dz = [0]

    for tower_stat in tower_stats_dict.values():
        try:
            x_pos.append(int(tower_stat.x_pos))
            y_pos.append(int(tower_stat.y_pos))
            z_pos.append(0)
            dx.append(20)
            dy.append(20)
            dz.append(int(tower_stat.pop_count))
        except:
            logger.critical('a tower_stat was passed')

            # logger.info('the value of x_pos are{}' + str(x_pos))


def update_plot_with_new_tower(x, y):
    """Draws a new 0-height bar at the positions x and y"""
    x_pos.append(x)
    y_pos.append(y)
    z_pos.append(0)

    dx.append(1)
    dy.append(1)
    dz.append(0)


def show_plot():
    plt.ion()
    # logger.debug('inside show_plot. x_pos is: ' + str(x_pos))
    ax1.bar3d(x_pos, y_pos, z_pos, dx, dy, dz)
    logger.debug('inside show_plot. x_pos are' + str(x_pos))
    plt.draw()
    plt.pause(0.001)



def try_machine_learning(tower_stats_dict):

    X = []  #this is the x,y position of all towers
    y = []  #this is their pop counts
    for tower_stat in tower_stats_dict.values():
        try:
            X.append([int(tower_stat.x_pos), int(tower_stat.y_pos)])
            y.append(int(tower_stat.pop_count))
        except:
            logger.critical('a tower_stat was passed')

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    predicted_value = knn.predict([50, 100])
    logger.info('predicting with [50, 100] :' + str(predicted_value[0]))

   
