import numpy as np
import math

from parameters import Parameters
from tiling import outputTiling
from gamma import MappedGammaParameter, MGPcentralSymetry, MGPnotExactSymetry, MGPdeBruijnRegular, MGPpentaville, MGPpentavilleS, MGPpentavilleVariation


#################################### uses all default parameters
def goSimple():
    outputTiling(Parameters())

    

###################################### with a fixed GAMMA value

SEQUENCE_LIVRET = [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)]

def goLivret():
    N = 5
    gamma = MappedGammaParameter(
        N=N,  # Size
        fixedGammaValue = np.array([-0.260, -0.155, -0.050, 0.055, 0.160]),
    )
    p = Parameters(
        GAMMA=gamma,
        N=N,
        SIDES = False,
        RECTANGLE = True,
        R=62,
        FRAME = True,
        SAVE=True,
        SAVE_FORMAT = 'pdf',
        SHOW=False,
        TILINGDIR="../Pavages/toto"
    )

    for (d, nbl) in SEQUENCE_LIVRET[:4]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputTiling(p)

            
###################################### with a varying GAMMA value
def goLivretVar():
    N = 5
    initialshift = 0.03
    gamma = MappedGammaParameter(
        N=N,  
        fixed = False,
        functionToMap=lambda s, j : s - 0.05 * j
    )
    p = Parameters(
        GAMMA=gamma,
        N=N,
        FRAME = True,
        DIAGONAL = True,
        SIDES = False,
        SHOW = False,
        SAVE=True,
        SAVE_FORMAT = 'pdf',
        TILINGDIR="../Pavages/toto"
    )

    while True:
        for (d, nbl) in SEQUENCE_LIVRET[:4]:
            p.NBL = nbl
            p.updateDMAX(d)
            outputTiling(p)

        gamma.setNextValue()

    


######################################
def goPolo(N, shift):
    gamma = MappedGammaParameter(
        N=N,
        fixed=False,
        initialShift=shift,
        functionToMap=lambda s, j: (s+j/5**1.03)+1)
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        R=0,
        DIAGONAL=True,
        COLORING = 15,
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        SAVE=True,
        SHOW=True,
        TILINGDIR="./poloTilings"
    )

    for (dmax, nbl) in [(15, 7),]:
        p.NBL = nbl
        p.updateDMAX(dmax)
        outputTiling(p)

###################################
def goCentralSymetry() :
    p = Parameters(GAMMA = MGPcentralSymetry)
    outputTiling(p)

def goNotExactSymetry() :
    p = Parameters(GAMMA = MGPnotExactSymetry)
    outputTiling(p)
 
def goDeBruijnRegular(N = 5):
    p = Parameters(
        GAMMA=MGPdeBruijnRegular(N),
        N=N)
    outputTiling(p)

def goPentaville() :
    N = 5
    gamma = MGPpentaville(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    outputTiling(p)
 
def goPentavilleS() :
    N = 5
    gamma = MGPpentavilleS(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    while True :
        outputTiling(p)
        gamma.setNextValue()

        
def goPentavilleVariation() :
    N = 5
    gamma = MGPpentavilleVariation(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        NBL = 8,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    while True :
        outputTiling(p)
        gamma.setNextValue()
 