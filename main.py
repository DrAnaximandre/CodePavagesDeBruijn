###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################

from go import *
from utils import ParallelProcessor

P = ParallelProcessor()
P.add(goPoloVideo)
P.run([i for i in range(60)])

#goLivret() # does not display but saves pdf
#goLivretVar() # does not display but saves pdf, and does not quit

# goCentralSymetry()
# goNotExactSymetry()
# goDeBruijnRegular(6)
# goPentaville()
# goPentavilleS()
# goPentavilleVariation()
