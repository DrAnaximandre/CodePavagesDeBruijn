from parameters import Parameters
from tiling import outputTiling
from gamma import MappedGammaParameter
import numpy as np

####################################
def goSimple(N, gammaValue):
    p = Parameters(
        N = N,
        GAMMA= MappedGammaParameter(
            N=N,
            gammaValue = gammaValue,
            shift = 0,
            deltashift = 0,
            a=0,
            functiontomap=lambda x: x
        )
    )

    outputTiling(p)

    

###################################### avec un GAMMA fixe
def goLivret():
    N = 5
    gamma = MappedGammaParameter(
        N=N,  # Size
        gammaValue = np.array([-0.260, -0.155, -0.050, 0.055, 0.160]),
        shift = 0,
        deltashift = 0,
        a=0,
        functiontomap=lambda x: x
    )
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        DIAGONAL = False,
        SIDES = False,
        RECTANGLE = True,
        R=62,
        SAVE=True,
        SAVE_FORMAT = 'pdf',
        SHOW=False,
        TILINGDIR="../Pavages/toto"
    )

    # for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)] :
    #for (d, nbl) in [(4, 3), (8, 6), (15, 8), (30, 16), (60, 33)]:
    for (d, nbl) in [(4, 3), (8, 6), (15, 8)]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputTiling(p)

            
###################################### avec un GAMMA variable
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
        N=gamma.N,
        DIAGONAL = False,
        SIDES = False,
        RECTANGLE = True,
        R=62,
        SAVE=True,
        SAVE_FORMAT = 'pdf',
        SHOW=False,
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
