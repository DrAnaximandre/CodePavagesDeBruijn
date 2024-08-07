import numpy as np

from parameters import Parameters
from tiling import outputTiling
import gamma as gm


#################################### uses all default parameters
def goAllDefaults(config=None):
    p = Parameters(**config.get('Parameters', {}))
    outputTiling(p)

    
#################################### a very small tiling
def goVerySmall(config=None):
    params = config.get('Parameters', {})
    params.update({'N': 5, 'DMAX': 2, 'NBL': 0})
    outputTiling(Parameters(**params))

    
###################################### with a fixed and initial GAMMA value

SEQUENCE_LIVRET = [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)]

def goLivret(config=None):
    """
    Generates a tiling with a fixed and initial GAMMA value.
    """
    N = 5
    initial_gamma_values = [-0.260, -0.155, -0.050, 0.055, 0.160]
    gamma = gm.MappedGammaParameter(
        N=N, 
        initialGammaValue=np.array(initial_gamma_values),
    )

    params = config.get('Parameters', {})
    params.update({
        "GAMMA":gamma,
        "N":N,
        "SIDES":False,
        "RECTANGLE":True,
        "R":62,
        "FRAME":True,
        "SHOW":False
    })
    p = Parameters(**params)

    for (d, nbl) in SEQUENCE_LIVRET[:4]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputTiling(p)

            
###################################### with a varying GAMMA value

def goLivretVar(config=None):
    N = 5
    
    gamma = gm.MappedGammaParameter(
        N=N,  
        functionToMap=lambda s, j : s - 0.05 * j
    )
    params = config.get('Parameters', {})
    params.update({
        "GAMMA":gamma,
        "N":N,
        "SIDES":False,
        "FRAME" : True,
        "DIAGONAL": True,
        "SIDES": False,
        "SHOW": False
    })

    p = Parameters(**params)

    for _ in range(4):
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
def goPoloCubes(s =1):
    """
    Go Polo! Cubes. Makes colorful cubes.
    """
    gamma = gm.MappedGammaParameter(
        N=6,
        initialShift=s,
        functionToMap=lambda s, j:  s if j%2 == 0 else -1.001 * j
    )
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=False,
        R=3,
        FRAME=False,
        DIAGONAL=False,
        SIDES=True,
        DMAX=20,
        NBL=12,
        COLORING=13,  # 16 uses a photo and "tiles" it, doesn't always work ...
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        SCALE_LINEWIDTH= 20,
        SAVE=True,
        TILINGDIR="./results/cubes",
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
        SIDES=True,
        DMAX=20,
        NBL=10,
        COLORING=13,  # 16 uses a photo and "tiles" it, doesn't always work ...
        BACKGROUND = 'k',
        STROKECOLOR= 'w',
        SCALE_LINEWIDTH= 12,
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
def goCentralSymetry(config=None):
    params = config.get('Parameters', {})
    params.update({'GAMMA': gm.MGPcentralSymetry()})
    outputTiling(Parameters(**params))

def goNotExactSymetry(config=None):
    params = config.get('Parameters', {})
    params.update({'GAMMA': gm.MGPnotExactSymetry()})
    outputTiling(Parameters(**params))
 
def goDeBruijnRegular(config=None):
    N = 5
    params = config.get('Parameters', {})
    params.update({'GAMMA': gm.MGPdeBruijnRegular(N), 'N': N})
    outputTiling(Parameters(**params))

def goPentaville(config=None) :
    N = 5
    params = config.get('Parameters', {})
    params.update({'GAMMA': gm.MGPpentaville(N),
                    'N': N, 
                    'DMAX': 12, 
                    'SIDES': False, 
                    'RECTANGLE': True, 
                    'R': 2, 
                    'FRAME': True})
    outputTiling(Parameters(**params))
 
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
        GAMMA = gm.MGPcentralSymetry(N,-0.0001),
        N=N,
        DMAX=40,
        NBL=20,
        SQUARE = True,
        OUTPUT_COORDINATES=True)
    outputTiling(p)
