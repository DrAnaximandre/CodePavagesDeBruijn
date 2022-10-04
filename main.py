##########################################################################
#
#  A simple implementation of the deBuijn method for non periodic tilings of the plane.
#
#  Bruijn, de, N. G. (1981). Algebraic theory of Penrose's non-periodic tilings of the plane.
#  Indagationes Mathematicae, 43(1), 39-66.
#
#  See also
#  https://github.com/neozhaoliang/pywonderland/blob/master/src/aperiodic-tilings/debruijn.py
#  for another implementation, much more "professional" and pythonic,
#  but with a different display style.
#
#  Another valuable site : https://www.mathpages.com/home/kmath621/kmath621.htm
#
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
