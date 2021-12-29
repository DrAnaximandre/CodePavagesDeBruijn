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

######################################

def goLivret() :

    gamma = MappedGammaParameter(
        N=5,  # Size
        shift=[-0.260, -0.155, -0.050, 0.055, 0.160],
        deltashift=[0 for _ in range(5)],
        a=0,
        functiontomap=lambda x: x
    )
    p = Parameters(
        GAMMA=gamma,
        N=5,
        R=62,
        SAVE=True,
        SHOW=False,
        RECTANGLE=True,
        TILINGDIR="./toto"
    )


    while True :

        #for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)] :
        for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33)] :
            p.NBL = nbl
            p.updateDMAX(d)
            outputNextTiling(p)
        
        p.nextGAMMA()


plt.ioff()


#go1()
goLivret()
