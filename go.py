import numpy as np

from parameters import Parameters
from tiling import outputTiling
import gamma as gm


#################################### uses all default parameters
def goAllDefaults():
    p = Parameters()
    outputTiling(p)

    
#################################### a very small tiling
def goVerySmall():
    outputTiling(Parameters(N=5,DMAX=2,NBL=0))

    
###################################### with a fixed and initial GAMMA value

SEQUENCE_LIVRET = [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)]

def goLivret():
    N = 5
    gamma = gm.MappedGammaParameter(
        N=N,  # Size
        initialGammaValue = np.array([-0.260, -0.155, -0.050, 0.055, 0.160]),
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
        SHOW=False
    )

    for (d, nbl) in SEQUENCE_LIVRET[:4]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputTiling(p)

            
###################################### with a varying GAMMA value

def goLivretVar():
    N = 5
    initialshift = 0.03
    gamma = gm.MappedGammaParameter(
        N=N,  
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
        SAVE_FORMAT = 'pdf'
    )

    for i in range(4):
        for (d, nbl) in SEQUENCE_LIVRET[:4]:
            p.NBL = nbl
            p.updateDMAX(d)
            outputTiling(p)

        gamma.setNextValue()


def goDemo(N=5):
    """
    goDemo is a demo of the tiling generator.
    It generates white patterns on a black background.

    """
    gamma = gm.MappedGammaParameter(
        N=N,
        initialShift=1.2345,
        functionToMap=lambda s, j:  2*np.sin(s-(1 + j) / N) + 0.1 * j /N + np.cos(j)/N
    )
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=True,
        SIDES=False,
        R=1,
        DMAX=25,
        NBL=25,
        COLORING=2,
        i=0,
        SAVE=True,
        SHOW=False,
        SAVE_FORMAT='png',
        TILINGDIR = "./results/demo",
        BACKGROUND = 'k',
        STROKECOLOR = 'w',
        SCALE_LINEWIDTH = 20
    )
    outputTiling(p)


######################################
def goPolo(N=4):
    """
    Go Polo! Go Polo!
    Generate and save pretty images.
    This is a test function, not a demo.
    """
    gamma = gm.MGPpentavilleVariation(N)
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=False,
        R=4,
        FRAME=False,
        DIAGONAL=False,
        SIDES=False,
        DMAX=20,
        NBL=10,
        COLORING=12,  # 16 uses a photo and "tiles" it, doesn't always work ...
        BACKGROUND = 'k',
        STROKECOLOR= 'w',
        SAVE=True,
        SHOW=True,
        IMAGEPATH="catinspace.png",
        DESTRUCTURED=False,
        FISHEYE=False,
        AUGMENTED_COLORS=False,
        TILINGDIR="./results",
        QUANTUM_COLOR=False, # very slow, much AI, consider small images
        i=123,
    )
    outputTiling(p)


###################################
def goCentralSymetry() :
    p = Parameters(GAMMA = gm.MGPcentralSymetry())
    outputTiling(p)

def goNotExactSymetry() :
    p = Parameters(GAMMA = gm.MGPnotExactSymetry())
    outputTiling(p)
 
def goDeBruijnRegular(N = 5):
    p = Parameters(
        GAMMA = gm.MGPdeBruijnRegular(N),
        N=N)
    outputTiling(p)

def goPentaville() :
    N = 5
    gamma = gm.MGPpentaville(N)
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
    gamma = gm.MGPpentavilleS(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    for i in range(4) :
        outputTiling(p)
        gamma.setNextValue()

        
def goPentavilleVariation() :
    N = 5
    gamma = gm.MGPpentavilleVariation(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        NBL = 8,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    for i in range(4) :
        outputTiling(p)
        gamma.setNextValue()

################################ Pour donner à manger au projet ..../Python/Grilles/grilArt2

def forGrilArt():
    N = 5
    p = Parameters(
        #GAMMA=MGPdeBruijnRegular(N),
        GAMMA = MGPcentralSymetry(N,-0.0001),
        N=N,
        DMAX=40,
        NBL=20,
        SQUARE = True,
        OUTPUT_COORDINATES=True)
    outputTiling(p)
