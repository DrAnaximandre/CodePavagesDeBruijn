##########################################################################
#
#  A simple implementation of the deBuijn method for non periodic tilings of the plane.
#
#  Bruijn, de, N. G. (1981). Algebraic theory of Penrose's non-periodic tilings of the plane.
#  Indagationes Mathematicae, 43(1), 39-66.
#
#  See also
#  https://github.com/neozhaoliang/pywonderland/blob/master/src/aperiodic-tilings/debruijn.py
#  for another implementation, much more "professional" and pythonic,
#  but with a different display style.
#
#  Another valuable site : https://www.mathpages.com/home/kmath621/kmath621.htm
#
###########################################################################
#  
#  Parameters can be adjusted, see the 'parameters' module.
#
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
#
##########################################################################
import matplotlib.pyplot as plt

from parameters import Parameters
from tiling import outputNextTiling
from gamma import MappedGammaParameter
import numpy as np


######################################

def goPolo():
    gamma = MappedGammaParameter(
        N=8,  # Size
        shift=np.array([10.5, 2, -15.2, 4, -5, 6, 2, 0.05]),
        deltashift=[0 for _ in range(8)],
        a=0,
        functiontomap=lambda x: 20*np.sin(2*x)
    )
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        R=0,
        SAVE=True,
        SHOW=True,
        RECTANGLE=False,
        BACKGROUND = "k",
        STROKECOLOR= "k",
        TILINGDIR="./toto"
    )

    for (d, nbl) in [(10,5), (15,12)]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputNextTiling(p)


goPolo()
