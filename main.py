###########################################################################
#  
#  Parameters can be adjusted, see the 'parameters' module.
#
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
#
##########################################################################
import tqdm
from joblib import Parallel,delayed
from go import *

kappa = 1 # number of images you want to run in parallel.
# This loops over
L = Parallel(n_jobs=-2)(
    delayed(goPolo)(5,
                    shift*10,
                    i) for
    i, shift in enumerate(range(kappa))
)


# goPolo3D(13,
#          0.0001,
#          0.5)

#goSimple()
#goPolo()
#goLivret() # does not display but saves pdf
#goLivretVar() # does not display but saves pdf, and does not quit

# goCentralSymetry()
# goNotExactSymetry()
# goDeBruijnRegular(6)
# goPentaville()
# goPentavilleS()
# goPentavilleVariation()
