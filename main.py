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
###########################################################################
#  
#  Parameters can be adjusted, see the 'parameters' module.
#
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
#
##########################################################################

import go

# L = Parallel(n_jobs=-2)(delayed(goPolo)(n+5, 5*np.sin(n), i) for i, n in enumerate(range(8, 9)))

#go.goPolo(5, -1, 0)

#go.allDefaults() # uses all defaults
#go.verySmall()
#goPolo()
#go.goLivret() # does not display but saves pdf
#goLivretVar() # does not display but saves pdf, and does not quit

#go.goCentralSymetry()
#go.goNotExactSymetry()
#go.goDeBruijnRegular(7)
#go.goPentaville()  # arranger le cadre
#go.goPentavilleS() # arranger la sortie
#go.goPentavilleVariation()

go.forGrilArt()  # liaison avec le projer GrilArt (TSP)
