from typing import Iterable
from joblib import Parallel,delayed

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
