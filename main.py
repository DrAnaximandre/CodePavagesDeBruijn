###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################

import go
from utils import ParallelProcessor
import numpy as np

###########  Polo's

#go.demo()
#go.Polo3D()
#go.Polo()
#go.PoloVideo()
goPoloCubes(3)
#P = ParallelProcessor()
#P.add(go.demo)
#P.run([3, 4, 5, 7, 9]) 



########## Mike's

#go.allDefaults() # uses all defaults
#go.verySmall()
#go.rectangles()

#go.colored()
#go.photo_default() 
#go.photos()

#go.livret() # does not display but saves pdf
#go.livretVar() # does not display but saves pdf

#go.centralSymetry()
#go.notExactSymetry()
#go.DeBruijnRegular(6)
#go.pentaville()
#go.pentavilleS()
#go.pentavilleVariation()

############### New features

#go.test()    # test et demo des principales fonctions
#go.neighbours(DMAX=15,NBL=10)

#
# P = ParallelProcessor()
# P.add(go.neighbours2)
# P.run(np.arange(-1, 1, 0.05))

#go.neighbours2(k=-1.215, DMAX=13,NBL=8)

go.neighbours2(k=0.215, DMAX=16,NBL=12)
#go.neighbours2(0.25)
