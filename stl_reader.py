from os import PathLike, path
from typing import Union
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import struct
import time

HEADER_BYTES = 84
COMMENT_SIZE_IN_HEADER = 80
BYTES_BY_TRIANGLE = 50
BLOCK_SIZE = 12
NUMBER_OF_BLOCKS = 4
CONTROL_BYTES = 2

def readSTL(file: Union[str, PathLike], unique=True, return_triangles=False, return_number_of_triangles=False, return_normals=False):
    """
    ## Reads a binary STL file and extracts all points from it.

    file: Union[str, PathLike] :\n
    Takes a path of a STL file and checks if it exists. Must include the ".stl" in the path

    ### kwargs :
    - unique makes function return unique points in ascendent order of x's. True by default
    - return_triangles makes function return every triangle in file in an array. False by default
    - return_number_of_triangles makes function return each normal of each triangle. False by default
    - return_normals makes function return number of triangles. False by default

    ### Return : 
    A numpy array with points or a python array [points, normals, number_of_triangles] depending on kwargs.\n
    If triangles data is returned, points array is replaces by triangles data.
    """
    if path.exists(file) and file.endswith(".stl"):
        in_file = open(file, 'rb')
        header = in_file.read(HEADER_BYTES)
        triangles_bytes = header[-(HEADER_BYTES - COMMENT_SIZE_IN_HEADER):]

        # Get number of triangles
        return_number_of_triangles = 0
        for c in range(len(triangles_bytes)):
            return_number_of_triangles += triangles_bytes[c] << (c * 8)

        file_buffer = in_file.read(50*return_number_of_triangles)

        triangles_data_array = np.array(list(struct.iter_unpack("ffffffffffffH", file_buffer)), dtype=np.float32)
        in_file.close()

        sub_arrays = np.hsplit(triangles_data_array, np.array([3,6,9,12,13]))
        normals = sub_arrays[0]
        points1 = sub_arrays[1]
        points2 = sub_arrays[2]
        points3 = sub_arrays[3]

        r = []

        p = np.concatenate((points1, points2, points3))

        if unique and not return_triangles:
            points1 = np.unique(p, axis=0)

        if return_triangles:
            triangles = np.concatenate((points1, points2, points3), axis=1)
            r.append(triangles)
        else:
            r.append(p)

        if return_normals:
            r.append(normals)

        if return_number_of_triangles:
            r.append(return_number_of_triangles)

        return r

def exportPointsAsMatplotlibPlotImage(points: np.ndarray, path: Union[str, PathLike], color_map="rainbow"):
    """
    ## Exports points array into a .png at a specified path

    - points : the points array read from readSTL funtion
    - path : the path where the file should be exported. e.g. : 'myfolder/img.png' or with os.path
    - color_map : the color map to use to render the [color](https://matplotlib.org/stable/gallery/color/colormap_reference.html)

    By default, color scale is based on x*y coordinates, you can only change this by changing cNorm in code.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    swappedArray = np.swapaxes(points, 1, 0)
    x, y, z = swappedArray
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    # Changes color of a 3D plot (stackoverflow)
    cm = plt.get_cmap(color_map)
    cNorm = mpl.colors.Normalize(vmin=min(x*y), vmax=max(x*y))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    # Creates a fake bounding box arround plot to scale axes 3d properly (thx stackoverflow)
    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
    ax.set(xlim=(Xb.min(), Xb.max()), ylim=(Yb.min(), Yb.max()), zlim=(Zb.min(), Zb.max()))
    ax.scatter(x, y ,z, c=scalarMap.to_rgba(x*y))
    plt.savefig(path)

if __name__ == "__main__":
    clock1 = time.time()
    points, normals, triangles = enumerate(readSTL("stlTest.stl", return_triangles=True, unique=False, return_normals=True, return_number_of_triangles=True))
    print(points)
    print(normals)
    print(triangles)
    print(time.time() - clock1)
