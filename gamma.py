import numpy as np
import math
from dataclasses import dataclass
from typing import Callable

##########################################

def mapR(x, xD, xF, yD, yF) :
    return yD + (yF-yD)/(xF-xD)*(x-xD)


@dataclass
class MappedGammaParameter(object) :
 
    def __init__(self,
                 N: int = 5, # Size
                 fixedGammaValue : np.ndarray = [-0.260, -0.155, -0.050, 0.055, 0.160],
                 fixed : bool = True,
                 initialShift : float = 2.01,
                 deltaShift: float = 0.025,
                 functionToMap: Callable = lambda s,j : s
                ):

        self.N = N
        self.gammaValue = fixedGammaValue if fixed else [functionToMap(initialShift,j) for j in range(self.N)]
        self.shift = initialShift
        self.deltaShift = deltaShift
        #self.a = a
        self.functionToMap = functionToMap
        

    def getValue(self):
        return self.gammaValue

    def setNextValue(self):
        self.shift -= self.deltaShift
        self.gammaValue = [self.functionToMap(self.shift,j) for j in range(self.N)]
        
    def string(self):
        s = "GAMMA="
        for x in self.gammaValue:
            s += ("%+.3f" % x)
        return s

    def stringTex(self) :
        g = self.gammaValue
        s = "$\gamma=[" + ("%+.3f" % g[0]) 
        for i in range(1,self.N) :
            s += (",%+.3f" % g[i])
        return s+']$'


#################### choix possibles pour gammaValue (ancien code reformulé dans le nouveau)


    # Gives a tiling with perfect central symetry,
    #  but 'singular' in the deBruijn sense.
    # self.GAMMA = [self.SHIFT] * self.N
MGPcentralSymetry = MappedGammaParameter(
    fixed = False)



    # Tilings could be not exactly symetric
    # self.GAMMA = [self.SHIFT - 0.00085 * j for j in range(self.N)]
    # self.GAMMA = [self.SHIFT - 0.05 * j for j in range(self.N)]
MGPnotExactSymetry = MappedGammaParameter(
    fixed = False,
    functionToMap = lambda s, j :  s - 0.05 * j)




    # More or less enforces the deBruijn 'regular' conditions for the tiling
    #   (see the paper, and the 'mathpage' site).
    # Better aspect with small DMAX (i.e. 7) and screen entirely filled.
    # self.GAMMA = [mapR(j, 0, self.N-1, -0.29 + self.SHIFT, 0.19 - self.SHIFT) for j in range(self.N)]
def MGPdeBruijnRegular(N) :
    return MappedGammaParameter(
        fixed = False,
        functionToMap = lambda s, j : mapR(j, 0, N-1, -0.29 + s, 0.19 - s)   )



    # special "Pentaville" (best for N=5, large DMAX, screen entirely filled)
    # -- always gives the same tilling ! (does not depend on SHIFT)
    # self.GAMMA = [math.sin(j*math.pi/self.N) for j in range(self.N)]
def MGPpentaville(N):
    return MappedGammaParameter(
        fixed = False,
        functionToMap = lambda s, j : math.sin(j*math.pi/N)   ) 
    
    # the same but now depends on shift (more interesting)
def MGPpentavilleS(N):
    return MappedGammaParameter(
        fixed = False,
        functionToMap = lambda s, j : math.sin(j*math.pi/N) + s  ) 
 


    # -- variation of pentaville
    # self.GAMMA = [math.sin((j+1)*math.pi/self.N) + j*self.SHIFT/self.N for j in range(self.N)]
def MGPpentavilleVariation(N):
    return MappedGammaParameter(
        fixed = False,
        initialShift = 1.07,
        deltaShift = 0.08,
        functionToMap = lambda s, j : math.sin(j*math.pi/N) + j/N + s) 




    # for livret #2 (avec DIAGONALS) with N=5
    # self.GAMMA = [0.0, 0.486, 0.747, 0.645, 0.180]

# use fixed = True and corresponding fixedGammaValue (see default value)

    # for livret #3 with R=2 (ancienne valeur, elle a pu changer) pour N=5
    # self.GAMMA = [1.890, 1.885, 1.880, 1.875, 1.870]

    # pour livret #4 avec R = 62 et N = 5
    #self.GAMMA = [-0.260, -0.155, -0.050, 0.055, 0.160]
