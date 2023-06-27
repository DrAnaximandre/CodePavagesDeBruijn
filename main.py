###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################


from go import *
from utils import ParallelProcessor

###########  Polo's

#goDemo()
#goPolo3D()
#goPolo()
#goPoloVideo()

#P = ParallelProcessor()
#P.add(goDemo)
#P.run([3, 4, 5, 7, 9])


gamma = gm.MappedGammaParameter(
    N=12,
    initialShift=np.pi,
    functionToMap=lambda s, j: s+j/8
)

p = Parameters(GAMMA=gamma,
               R=1,
               N = gamma.N,
               NBL=12,
               DMAX=15,
               COLORING=2,
               BACKGROUND='k',
               STROKECOLOR='r',
               SCALE_LINEWIDTH=10,
               RECTANGLE=True,
               DIAGONAL=False,
               SIDES=False,
               SAVE=True,
               SQUARE=True,
               SAVE_FORMAT='png',
               TITLE=False,
               FRAME=True,
               OUTPUT_COORDINATES=True,
               TILINGDIR="./results/27-juin")
outputTiling(p)


########## Mike's

#goAllDefaults() # uses all defaults
#goVerySmall()

#goLivret() # does not display but saves pdf
#goLivretVar() # does not display but saves pdf, and does not quit

#goCentralSymetry()
#goNotExactSymetry()
#goDeBruijnRegular(6)
#goPentaville()
#goPentavilleS()
#goPentavilleVariation()
