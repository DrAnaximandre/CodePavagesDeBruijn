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
    N=5,
    initialShift=0,
    functionToMap=lambda s, j: s+j*0.7
)

p = Parameters(GAMMA=gamma,
               R=1,
               COLORING=2,
               BACKGROUND='k',
               STROKECOLOR='w',
               SCALE_LINEWIDTH=20,
               RECTANGLE=True,
               DIAGONAL=False,
               SIDES=False,
               SAVE=True,
               TILINGDIR="./results/repro-18-juin")
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
