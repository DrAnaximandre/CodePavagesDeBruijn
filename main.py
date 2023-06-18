###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################

from go import *
from utils import ParallelProcessor

P = ParallelProcessor(n_jobs=-3)
P.add(goDemo)
P.run([5])

# make a video with the following command:
# ffmpeg -framerate 1 -i %d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4

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

#forGrilArt()  # liaison avec le projer GrilArt (TSP)

#goDemo()
#goPolo3D()
#goPolo()
#goPoloVideo()
