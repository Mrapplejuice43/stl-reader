import stl_reader
import transform_stl
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def generateStone(xRadius=50., yRadius=50., zRadius=50., res=101, export_figure=False) -> np.ndarray:
    x, y = np.linspace(-xRadius, xRadius, res), np.linspace(-yRadius, yRadius, res)
    xv, yv = np.meshgrid(x, y)
    z = np.sqrt(zRadius**2 * (1 - (xv**2)/(xRadius**2) - (yv**2)/(yRadius**2)))
    
    # points_arr = np.array([[0,0,0]])
    # for i in range(len(x)):
    #     for j in range(len(y)):
    #         p = z[i][j]
    #         if np.isnan(p):
    #             points_arr = np.concatenate((points_arr,[[x[i], y[j], 0.]]), axis=0)
    #         else:
    #             points_arr = np.concatenate((points_arr,[[x[i], y[j], p]]), axis=0)

    nb_points = len(x)*len(y)
    x_coords_arr = np.reshape(yv.flatten(), (1, nb_points))
    y_coords_arr = np.reshape(xv.flatten(), (1, nb_points))
    z_coords_arr = np.reshape(z.flatten(), (1, nb_points))
    points_arr = np.concatenate((x_coords_arr.T, y_coords_arr.T, z_coords_arr.T), axis=1)
    points_arr[np.isnan(points_arr)] = 0.

    if export_figure:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        cmin, cmax = min(xRadius, yRadius), max(xRadius, yRadius)
        ax.set(xlim=(-cmax,cmax), ylim=(-cmax,cmax), zlim=(0,cmax))
        ax.plot_wireframe(xv,yv,z)
        plt.savefig("stone_wireframe")
    return points_arr

if __name__ == "__main__":
    z = generateStone(500, 500, 200, 2001, export_figure=True)
    print(z)