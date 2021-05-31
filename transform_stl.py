import numpy as np
import stl_reader
import time
from math import radians, pi
import matplotlib as mpl
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rotatePoints(points: np.ndarray, xAngle=0., yAngle=0., zAngle=0., degrees=False, order="xyz") -> np.ndarray:
    """
    ## Rotates point of a given array.
    ## IMPORTANT
    x-axis rotation has priority over y-axis rotation and y-axis rotation has priority over z-axis rotation.
    You will have to change order to give priority to different axes.

    This means that all points will rotate arround x, then arround y then arround z.

    points : List of points to be rotated
    xAngle : Rotation arround x-axis in radians
    yAngle : Rotation arround y-axis in radians
    zAngle : Rotation arround z-axis in radians

    degrees (optional) : If true uses angles in degrees. False by default
    order (optional) : The priority given to axes. "xyz" by default. If the given argurment doesn't correspond to a right order it applies default "xyz" priority

    Returns the array with rotation applied. 
    """
    if xAngle == yAngle == zAngle == 0.:
        return points

    if degrees:
        xAngle = radians(xAngle)
        yAngle = radians(yAngle)
        zAngle = radians(zAngle)
    
    xRotationMatrix = np.matrixlib.asmatrix(np.array([
        [1, 0, 0],
        [0, np.cos(xAngle), -np.sin(xAngle)],
        [0, np.sin(xAngle), np.cos(xAngle)]
    ]))

    yRotationMatrix = np.matrixlib.asmatrix(np.array([
        [np.cos(yAngle), 0, np.sin(yAngle)],
        [0, 1, 0],
        [-np.sin(yAngle), 0, np.cos(yAngle)]
    ]))

    zRotationMatrix = np.matrixlib.asmatrix(np.array([
        [np.cos(zAngle), -np.sin(zAngle), 0],
        [np.sin(zAngle), np.cos(zAngle), 0],
        [0, 0, 1]
    ]))

    if order == "xzy":
        points = points * xRotationMatrix * zRotationMatrix * yRotationMatrix
    elif order == "yzx":
        points = points * yRotationMatrix * zRotationMatrix * xRotationMatrix
    elif order == "yxz":
        points = points * yRotationMatrix * xRotationMatrix * zRotationMatrix
    elif order == "zxy":
        points = points * zRotationMatrix * xRotationMatrix * yRotationMatrix
    elif order == "zyx":
        points = points * zRotationMatrix * yRotationMatrix * xRotationMatrix
    else: 
        points = points * xRotationMatrix * yRotationMatrix * zRotationMatrix

    return np.array(points)


def translatePoints(points: np.ndarray, x=0, y=0, z=0, unit=None) -> np.ndarray:
    """
    ## Translates whole STL in a given direction
    ## Important :
    As rotation doesn't rotate the coordinate system, if you apply translation after the rotation it will move the points in the absolute coordinate system not in the "object's" one.

    x, y, z : translation in the given direction
    unit (optional) : useless at the moment

    Returns the array with translation applied.
    """
    if x == y == z == 0:
        return points

    return points + np.array([x,y,z])

def scalePoints(points: np.ndarray, x=1., y=1., z=1., conservative=False) -> np.ndarray:
    """
    ## Scales whole STL in a given direction
    ## Important :
    As rotation doesn't rotate the coordinate system, if you apply scaling after the rotation it will move the points in the absolute coordinate system not in the "object's" one.

    x, y, z : ration applied in the given direction
    conservative (optional) : Makes funcion apply x's scaling in every direction.

    Returns the array with scaling applied.
    """
    if conservative:
        return points * [x, x, x]

    return points * [x,y,z]

if __name__ == "__main__":
    points = stl_reader.readSTL("thanos.stl")
    c1 = time.time()
    points = translatePoints(points, x=0, y=0, z=0)
    points = scalePoints(points, 1, conservative=True)
    points = rotatePoints(points, xAngle=0., yAngle=0., zAngle=0., degrees=True, order="xyz")
    print(time.time() - c1)

    c1 = time.time()
    stl_reader.exportPointsAsMatplotlibPlotImage(points, "test", color_map="viridis")
    print(time.time() - c1)