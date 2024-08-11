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
    params.update({'DMAX': 2, 'NBL': 0})
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

    if 'N' in params:
        print("N is provided in the config file but this go function is designed for N=5 ")

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

    if 'N' in params:
        print("N is provided in the config file but this go function is designed for N=5 ")

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

    if 'N' in params:
        print("N is provided in the config file but this go function is designed for N=5 ")

    params.update({'GAMMA': gm.MGPdeBruijnRegular(N), 'N': N})
    outputTiling(Parameters(**params))

def goPentaville(config=None) :
    N = 5
    params = config.get('Parameters', {})

    if 'N' in params:
        print("N is provided in the config file but this go function is designed for N=5 ")

    params.update({'GAMMA': gm.MGPpentaville(N),
                    'N': N, 
                    'DMAX': 12, 
                    'SIDES': False, 
                    'RECTANGLE': True, 
                    'R': 2, 
                    'FRAME': True})
    outputTiling(Parameters(**params))
 
def goPentavilleS(config) :
    N = 5
    params = config.get('Parameters', {})
    gamma = gm.MGPpentavilleS(N)

    if 'N' in params:
        print("N is provided in the config file but this go function is designed for N=5 ")

    params.update({'GAMMA': gamma,
                    'N': N, 
                    'DMAX': 12, 
                    'SIDES': False, 
                    'RECTANGLE': True, 
                    'R': 2, 
                    'FRAME': True})
    p = Parameters(**params)
    for _ in range(4) :
        outputTiling(p)
        gamma.setNextValue()
        params.update({'GAMMA': gamma})
        p = Parameters(**params)

        
def goPentavilleVariation(config) :
    N = 5
    params = config.get('Parameters', {})

    if 'N' in params:
        print("N is provided in the config file but this go function is designed for N=5 ")

    gamma = gm.MGPpentavilleVariation(N)
    params.update({'GAMMA': gamma,
                    'N': N, 
                    'DMAX': 12, 
                    'NBL': 8,
                    'SIDES': False, 
                    'RECTANGLE': True, 
                    'R': 2, 
                    'FRAME': True})
    p = Parameters(**params)
    outputTiling(p)
        

def goDemo(config=None):
    """
    goDemo is a demo of the tiling generator.
    It generates white patterns on a black background.

    """
    params = config.get('Parameters', {})
    gamma = gm.MappedGammaParameter(
        N=params['N'],
        initialShift=1.2345,
        functionToMap=lambda s, j:  2*np.sin(s-(1 + j) / params['N']) + 0.1 * j /params['N'] + np.cos(j)/params['N']
    )

    params.update({'GAMMA': gamma, 
                    'DMAX': 25,
                    'NBL': 25,
                    'SIDES': False,
                    'RECTANGLE': True,
                    'R': 1,
                    'COLORING': 2,
                    'FRAME': False,
                    'BACKGROUND': 'k',
                    'STROKECOLOR': 'w',
                    'SCALE_LINEWIDTH': 20,
                    })
    outputTiling(Parameters(**params))

######################################
def goPoloCubes(config=None):
    """
    Go Polo! Cubes. Makes colorful cubes.
    """
    params = config.get('Parameters', {})

    gamma = gm.MappedGammaParameter(
        N=params['N'],
        initialShift=0.1,
        functionToMap=lambda s, j:  s if j%2 == 0 else -1.001 * j
    )

    params.update({'GAMMA': gamma, 
                    'DMAX': 20, 
                    'NBL': 12,
                    'SIDES': True, 
                    'RECTANGLE': False, 
                    'R': 3, 
                    'FRAME': False,
                    'DIAGONAL': False,
                    'COLORING': 13,
                    'BACKGROUND': 'k',
                    'STROKECOLOR': 'k',
                    'SCALE_LINEWIDTH': 20,
                    'SHOW': True,
                    })
    outputTiling(Parameters(**params))


######################################
def goPolo(config=None):
    """
    Go Polo! Go Polo!
    Generate and save pretty images.
    """
    params = config.get('Parameters', {})
    params.update({'GAMMA': gm.MGPpentavilleVariation(params['N']),
                    'DMAX': 20, 
                    'NBL': 10,
                    'SIDES': False, 
                    'RECTANGLE': False, 
                    'R': 4, 
                    'FRAME': False,
                    'DIAGONAL': False,
                    'COLORING': 13,
                    'BACKGROUND': 'k',
                    'STROKECOLOR': 'w',
                    'SCALE_LINEWIDTH': 12,
                    'SHOW': False,
                    })
    outputTiling(Parameters(**params))

       

################################ Pour donner à manger au projet ..../Python/Grilles/grilArt2

def forGrilArt():
    N = 5
    p = Parameters(
        GAMMA = gm.MGPcentralSymetry(N,-0.0001),
        N=N,
        DMAX=40,
        NBL=20,
        SQUARE = True,
        OUTPUT_COORDINATES=True)
    outputTiling(p)
