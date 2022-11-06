import numpy as np

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

    
def goPolo3D(N=4, shift=1, i=1234, dmax=5, nbl=5):
    gamma = MappedGammaParameter(
        N=N,
        fixed=False,
        initialShift=shift,
        functionToMap=lambda s, j : s*np.sin((1+j)/5)) #/(1+j))
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=False,
        R=3,
        DIAGONAL=False,
        SIDES=True,
        COLORING=0,
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        SAVE=True,
        SHOW=True,
        IMAGEPATH="start/fleurs.jpg",
        DESTRUCTURED=False,
        FISHEYE=False,
        AUGMENTED_COLORS=False,
        TILINGDIR="./results",
        QUANTUM_COLOR=False,
        i=i,
        SAVELOP=True
    )

    p.magic = shift
    p.NBL = nbl
    p.updateDMAX(dmax)
    outputTiling(p)


######################################
def goPolo(N=4, # N=4 is for a squarish feeling?
           shift=1, # shift ?
           i=1234 # I think it should be used for file naming)?
           ):
    """
    Go Polo! Go Polo!

    Generate and save pretty images.


    """
    gamma = MappedGammaParameter(
        N=N, # N ? 3 is triangle, 4 is squarish, 5 is cool and pentagonal, 6 has stars
        fixed=False,
        initialShift=shift, # shift ?
        functionToMap=lambda s, j : (4+s)*np.cos(j*10))
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=False,
        R=4,
        DIAGONAL=False,
        SIDES=True,
        COLORING=15,  # 16 uses a photo and "tiles" it, doesn't always work ...
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        SAVE=True,
        SHOW=True,
        IMAGEPATH="catinspace.png",
        DESTRUCTURED=False,
        FISHEYE=False,
        AUGMENTED_COLORS=False,
        TILINGDIR="./results",
        QUANTUM_COLOR=False, # very slow, much AI, consider small images
        i=i
    )

    for (dmax, nbl) in [(25,
                         14)]:
        p.magic = shift  # seriously ?
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
 