from typing import Iterable
from joblib import Parallel,delayed

#-------------------------- ce bout de code est buggué, je remets le mien en attendant de trouver le bug
# def middles(xs, ys):
#
#     res = []
#     for i in range(4):
#         for j in range(4):
#             if i == (j+1)%4 :
#
#                 nx = (xs[i] + xs[j])/2
#                 ny = (ys[i] + ys[j])/2
#                 print(i,j)
#                 res.append(nx)
#                 res.append(ny)
#
#     return res



def middle(x1, y1, x2, y2):
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0

def middles(xs, ys):
    x01, y01 = middle(xs[0], ys[0], xs[1], ys[1])
    x12, y12 = middle(xs[1], ys[1], xs[2], ys[2])
    x23, y23 = middle(xs[2], ys[2], xs[3], ys[3])
    x30, y30 = middle(xs[0], ys[0], xs[3], ys[3])
    return x01, y01, x12, y12, x23, y23, x30, y30


def linearPoint(A,B,k):
    xA,yA = A
    xB,yB = B
    xC = xA + (xB-xA)*k
    yC = yA + (yB-yA)*k
    return (xC,yC)
    

def mapR(x: float, xD: float, xF: float, yD: float, yF: float) -> float:
    """
    Perform linear interpolation to map a value `x` from one range [xD, xF] to another range [yD, yF].

    Args:
        x (float): The value to map.
       xD (float): The lower bound of the input range.
       xF (float): The upper bound of the input range.
       yD (float): The lower bound of the output range.
       yF (float): The upper bound of the output range.

    Returns:
       float: The mapped value in the output range.
    """
    return yD + (yF-yD)/(xF-xD)*(x-xD)

class ParallelProcessor:
    """ This is a class to run several go functions in parallel.

    Example:
        P = ParallelProcessor()
        P.add(goDemo)
        P.run([4, 5, 7])
    """

    def __init__(self, n_jobs=-1):
        """ n_jobs is the number of jobs to run in parallel. -1 means all CPUs"""
        self.gos = []
        self.n_jobs = n_jobs

    def add(self, go):
        """ Add a go function to the list of functions to run in parallel"""
        self.gos.append(go)

    def run(self, kappa: Iterable[float]):
        """ Run all the go functions in parallel with the given kappa values

        kappa is a list of kappa values to run the go functions with.
        By default, the go functions are run with the same kappa values
        """
        delayed_gos = (delayed(g)(k) for g in self.gos for k in kappa)
        Parallel(n_jobs=self.n_jobs)(delayed_gos)
