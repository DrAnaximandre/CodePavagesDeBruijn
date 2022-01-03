import numpy as np

from parameters import Parameters
from tiling import outputTiling
from gamma import MappedGammaParameter


#################################### uses all default parameters
def goSimple():
    outputTiling(Parameters())

    

###################################### with a fixed GAMMA value
def goLivret():
    N = 5
    gamma = MappedGammaParameter(
        N=N,  # Size
        gammaValue = np.array([-0.260, -0.155, -0.050, 0.055, 0.160]),
    )
    p = Parameters(
        GAMMA=gamma,
        N=N,
        DIAGONAL = False,
        SIDES = False,
        RECTANGLE = True,
        R=62,
        FRAME = True,
        SAVE=False,
        SAVE_FORMAT = 'pdf',
        SHOW=True,
        TILINGDIR="../Pavages/toto"
    )

    # for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)] :
    #for (d, nbl) in [(4, 3), (8, 6), (15, 8), (30, 16), (60, 33)]:
    for (d, nbl) in [(4, 3), (8, 6), (15, 8)]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputTiling(p)

            
###################################### with an evolving GAMMA value
def goLivretVar():
    N = 5
    initialshift = 0.03
    gamma = MappedGammaParameter(
        N=N,  # Size
        shift = initialshift,
        deltashift = 0.1,
        gammaValue = [initialshift]*N,
        a=0,
        functiontomap=lambda x: x
    )
    p = Parameters(
        GAMMA=gamma,
        N=N,
        FRAME = True,
        DIAGONAL = False,
        SIDES = False,
        RECTANGLE = True,
        R=62,
        SAVE=False,
        SAVE_FORMAT = 'pdf',
        SHOW=True,
        TILINGDIR="../Pavages/toto"
    )

    while True:
        # for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)] :
        #for (d, nbl) in [(4, 3), (8, 6), (15, 8), (30, 16), (60, 33)]:
        for (d, nbl) in [(4, 3), (8, 6), (15, 8)]:
            p.NBL = nbl
            p.updateDMAX(d)
            outputTiling(p)

        gamma.setNextValue()

        




######################################
def goPolo():
    gamma = MappedGammaParameter(
        N=8,  # Size
        gammaValue=np.array([10.5, 2, -15.2, 4, -5, 6, 2, 0.05]),
        shift = 0,
        deltashift=[0 for _ in range(8)],  # A REPRENDRE
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
        DIAGONAL=True,
        COLORING = 11,
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        TILINGDIR="../Pavages/poloTilings"
    )

    for (d, nbl) in [(10,5), (15,12)]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputTiling(p)
