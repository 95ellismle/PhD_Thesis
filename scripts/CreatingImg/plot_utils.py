import matplotlib.pyplot as plt
import numpy as np


BLUE = (0.3, 0.4, 1)
RED = (1, 0.3, 0.4)
GREY = (0.3, 0.3, 0.3)

ANNOTATE_FONTSIZE = 27



def create_arrow(xy, size=0.7, prop_angle=30):
    """
    Will draw an arrow with matplotlib

    Inputs:
        * axis <plt.axis> => The axis on which to draw the arrow
        * xy <tuple(x, y)> => The position to draw the arrow tip
        * size <float|int> => How big to draw the arrow props
        * prop_angle <float|int> => What angle to draw the props at (degrees)

    Outputs:
        * <tuple(list x, list y)> The list of points to plot to create the specified arrow.
    """
    Ox, Oy = xy
    angle = prop_angle * np.pi/ 180
    x = [Ox-size*np.cos(angle), Ox, Ox-size*np.cos(angle)]
    y = [Oy-size*np.sin(angle), Oy, Oy+size*np.sin(angle)]

    return x, y


def rot_points_2D(xy, rot_angle, origin=(0, 0)):
    """
    Will rotate points on a 2D XY plane by a specified angle clockwise.

    Inputs:
        * xy <tuple(list x,  list y)> => The xy points in a tuple (2 lists of x and y floats or ints)
        * rot_angle <float|int> => The angle about which to rotate (degrees)
        * origin <tuple(x, y)> => The point of rotation (float or int x and y coords)

    Outputs:
        * <tuple(list x, list y)> The points rotated by specified angle.
    """
    theta = rot_angle * np.pi / 180.
    xy = np.array(list(xy))
    xy[0, :] -= origin[0]
    xy[1, :] -= origin[1]
    rot_mat = np.array([[np.cos(theta), -np.sin(theta)],
                        [np.sin(theta),  np.cos(theta)]])
    rot_pts = np.array([np.matmul(rot_mat, i) for i in xy.T])
    rot_pts = rot_pts.T
    rot_pts[0, :] += origin[0]
    rot_pts[1, :] += origin[1]
    return rot_pts


#import matplotlib.pyplot as plt
#
#
#
#x, y = create_arrow((0, 0.1), 1)
#plt.plot(x, y)
#
#i = 45
##for i in range(0, 92, 2):
#nx, ny = rot_points_2D((x, y), i, (np.mean(x), np.mean(y)))
#plt.plot(nx, ny)
#
#plt.xlim([-1.1, 1.1])
#plt.ylim([-1.1, 1.1])

plt.show()



