###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################

from go import *
from utils import ParallelProcessor

P = ParallelProcessor()
P.add(goDemo)
P.run([3, 4, 5, 7, 9])

#goLivret() # does not display but saves pdf
#goLivretVar() # does not display but saves pdf, and does not quit

# goCentralSymetry()
# goNotExactSymetry()
# goDeBruijnRegular(6)
# goPentaville()
# goPentavilleS()
# goPentavilleVariation()
