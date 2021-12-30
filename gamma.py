import numpy as np
from dataclasses import dataclass
from typing import Callable

@dataclass
class MappedGammaParameter:

    N: int # Size
    a: float

    shift: np.ndarray
    deltashift: np.ndarray

    functiontomap: Callable

    # Gives a tiling with perfect central symetry,
    #  but 'singular' in the deBruijn sense.
    # self.GAMMA = [self.SHIFT] * self.N

    # Tilings could be not exactly symetric
    # self.GAMMA = [self.SHIFT - 0.00085 * j for j in range(self.N)]
    # self.GAMMA = [self.SHIFT - 0.05 * j for j in range(self.N)]

    # More or less enforces the deBruijn 'regular' conditions for the tiling
    #   (see the paper, and the 'mathpage' site).
    # Better aspect with small DMAX (i.e. 7) and screen entirely filled.
    # self.GAMMA = [mapR(j, 0, self.N-1, -0.29 + self.SHIFT, 0.19 - self.SHIFT) for j in range(self.N)]

    # special "Pentaville" (best for N=5, large DMAX, screen entirely filled)
    # -- always gives the same tilling ! (does not depend on SHIFT)
    # self.GAMMA = [math.sin(j*math.pi/self.N) for j in range(self.N)]
    # self.GAMMA = [math.sin((j+1)*math.pi/self.N) + j*self.SHIFT/self.N for j in range(self.N)]

    # for livret #2 (avec DIAGONALS) with N=5
    # self.GAMMA = [0.0, 0.486, 0.747, 0.645, 0.180]

    # for livret #3 with R=2 (ancienne valeur, elle a pu changer) pour N=5
    # self.GAMMA = [1.890, 1.885, 1.880, 1.875, 1.870]

    # pour livret #4 avec R = 62 et N = 5
    #self.GAMMA = [-0.260, -0.155, -0.050, 0.055, 0.160]


    def setGamma(self):
        return self.functiontomap(self.shift) - np.array([self.a * j for j in range(self.N)])

    def nextgamma(self):
        self.shift -= self.deltashift
