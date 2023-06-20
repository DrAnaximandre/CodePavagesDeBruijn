import numpy as np
import math
from dataclasses import dataclass
from typing import Callable

##########################################

# returns the y coordinates corresponding to the given x,
# so that the point (x,y) is on the DF line (linear interpolation)
def mapR(x, xD, xF, yD, yF) :
    return yD + (yF-yD)/(xF-xD)*(x-xD)

# a good value
def defaultGamma(N) :
    return [mapR(j, 0, N-1, -0.29, 0.19) for j in range(N)]
     
@dataclass
class MappedGammaParameter(object) :

    def __init__(self,
                 N: int = 5,
                 
                 # initialGammaValue defined later because of N dependancy
                 initialGammaValue : np.ndarray = None,
                 
                 initialShift : float = 2.01,
                 deltaShift: float = 0.025,

                 # functionToMap can be used to build the initial value and successive values
                 #  using setNextValue in a loop (see for ex. go.goLivretVar() )
                 functionToMap: Callable = None,

                ):

        self.N = N
        if initialGammaValue is not None :
            self.gammaValue = initialGammaValue
        elif functionToMap is not None :
            self.gammaValue = [functionToMap(initialShift,j) for j in range(N)]
        else :
            self.gammaValue = defaultGamma(N)
        self.shift = initialShift
        self.deltaShift = deltaShift
        self.functionToMap = functionToMap

    def getValue(self):
        return self.gammaValue

    def setNextValue(self):
        self.shift -= self.deltaShift
        self.gammaValue = [self.functionToMap(self.shift,j) for j in range(self.N)]
        
    def string(self):
        s = "GAMMA="
        for x in self.getValue() :
            s += ("%+.3f" % x)
        return s

    def stringTex(self) :
        g = getValue()
        s = "$\gamma=[" + ("%+.3f" % g[0]) 
        for i in range(1, self.N):
            s += (",%+.3f" % g[i])
        return s+']$'


#################### some choices for gammaValue


    # Gives a tiling with perfect central symetry,
    #  but 'singular' in the deBruijn sense.
def MGPcentralSymetry(N=5, shift=0.001) :
    return MappedGammaParameter(
        N=N,
        initialGammaValue = [shift] * N)

    # Tilings could be not exactly symetric
def MGPnotExactSymetry(N=5) :
    return MappedGammaParameter(
        N=N,
        functionToMap = lambda s, j :  s - 0.05 * j)

    # More or less enforces the deBruijn 'regular' conditions for the tiling
    #   (see the paper, and the 'mathpage' site).
    # Better aspect with small DMAX (i.e. 7) and screen entirely filled.
def MGPdeBruijnRegular(N) :
    return MappedGammaParameter(
        N=N,
        functionToMap=lambda s, j: mapR(j, 0, N-1, -0.29 + s, 0.19 - s))

    # special "Pentaville" (best for N=5, large DMAX, screen entirely filled)
    # -- always gives the same tilling ! (does not depend on SHIFT)
def MGPpentaville(N):
    return MappedGammaParameter(
        N=N,
        functionToMap = lambda s, j : math.sin(j*math.pi/N))
    
    # the same but now depends on shift (more interesting)
def MGPpentavilleS(N):
    return MappedGammaParameter(
        N=N,
        functionToMap = lambda s, j : math.sin(j*math.pi/N) + s)
 
    # -- variation of pentaville
def MGPpentavilleVariation(N):
    return MappedGammaParameter(
        N=N,
        initialShift = 1.07,
        deltaShift = 0.08,
        functionToMap = lambda s, j : math.sin(j*math.pi/N) + j/N + s) 


    # for livret #2 (avec DIAGONALS) with N=5
    # self.GAMMA = [0.0, 0.486, 0.747, 0.645, 0.180]

    # for livret #3 with R=2 (ancienne valeur, elle a pu changer) pour N=5
    # self.GAMMA = [1.890, 1.885, 1.880, 1.875, 1.870]

    # pour livret #4 avec R = 62 et N = 5
    #self.GAMMA = [-0.260, -0.155, -0.050, 0.055, 0.160]
