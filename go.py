import numpy as np
import math

from parameters import Parameters
from tiling import outputTiling
from gamma import MappedGammaParameter, MGPcentralSymetry, MGPnotExactSymetry, MGPdeBruijnRegular, MGPpentaville, MGPpentavilleS, MGPpentavilleVariation


#################################### uses all default parameters
def allDefaults():
    p = Parameters()
    outputTiling(p)

#################################### a very small tiling 
def verySmall():
    outputTiling(Parameters(N=5,DMAX=2,NBL=0))

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
        #TILINGDIR="../Pavages/toto"
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
        #TILINGDIR="../Pavages/toto"
    )

    while True:
        for (d, nbl) in SEQUENCE_LIVRET[:4]:
            p.NBL = nbl
            p.updateDMAX(d)
            outputTiling(p)

        gamma.setNextValue()

    

######################################
def goPolo(N, shift, i):
    gamma = MappedGammaParameter(
        N=N,
        fixed=False,
        initialShift=shift,
        functionToMap=lambda s, j : 15*np.sin((s-j*np.pi)**2)+(j**2)/10 +1)
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=True,
        R=3,
        DIAGONAL=False,
        SIDES=True,
        COLORING=19,
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        SAVE=True,
        SHOW=True,
        IMAGEPATH="start/fleurs.jpg",
        DESTRUCTURED=False,
        FISHEYE=False,
        AUGMENTED_COLORS=False,
        TILINGDIR="./toto",
        QUANTUM_COLOR=False,
        i=i
    )

    for (dmax, nbl) in [(18,12)]:
        p.magic = shift
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

################################ Pour donner à manger au projet ..../Python/Grilles/grilArt2

def forGrilArt():
    N = 6
    p = Parameters(
        GAMMA=MGPdeBruijnRegular(N),
        N=N,
        DMAX=6,
        NBL=2,
        OUTPUT_COORDINATES=True)
    outputTiling(p)

######################### un pb à corriger dans gamma.py, le N ne correspond pas
def pb():
    outputTiling(Parameters(N=7))    
