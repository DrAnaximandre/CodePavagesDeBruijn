from parameters import Parameters
from tiling import outputNextTiling
from gamma import MappedGammaParameter
import numpy as np


######################################
def goLivret():
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
        SAVE_FORMAT = 'pdf',
        SHOW=False,
        RECTANGLE=True,
        TILINGDIR="../Pavages/toto"
    )

    while True:

        # for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)] :
        #for (d, nbl) in [(4, 3), (8, 6), (15, 8), (30, 16), (60, 33)]:
        for (d, nbl) in [(4, 3), (8, 6), (15, 8)]:
            p.NBL = nbl
            p.updateDMAX(d)
            outputNextTiling(p)

        p.nextGAMMA()


######################################
def goPolo():
    gamma = MappedGammaParameter(
        N=8,  # Size
        shift=np.array([10.5, 2, -15.2, 4, -5, 6, 2, 0.05]),
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
        COLORING = 11,
        BACKGROUND = "k",
        STROKECOLOR= "k",
        TILINGDIR="./toto"
    )

    for (d, nbl) in [(10,5), (15,12)]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputNextTiling(p)
