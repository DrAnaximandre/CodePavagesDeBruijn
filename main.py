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

import matplotlib.pyplot as plt
import numpy as np

from parameters import Parameters 
from tiling import tiling
from outputs import filename, title

######################################

def outputNextTiling(params):

    fn = filename(params)
    print(fn)

    fig, ax = plt.subplots()
    plt.axis('equal')
    plt.axis('off')
    plt.title(title(params), fontsize = 8, y = 0, pad = -20.)
    dmax = params.DMAX
    lim = dmax * 0.9
    dr = lim 
    xmin, xmax, ymin, ymax = -lim, lim, -lim, lim
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    left, bottom, width, height = -dr, -dr, 2*dr, 2*dr
    p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth = 0.2)
    ax.add_patch(p)
    
    tiling(params)
    
        # save d'abord et show apres !
    if params.SAVE :
        plt.savefig(fn + ".pdf" , bbox_inches="tight")
    if params.SHOW :
        plt.show()

    plt.close()



def go1() :
    p = Parameters()
    p.TILINGDIR = "../Pavages/toto"
    p.N = 5
    p.SAVE, p.SHOW = False, True
    p.RECTANGLE == True
    p.R == 0
    p.FILL == 0
    p.setGAMMA()
    print("p.GAMMA=" + str(p.GAMMA) + " p.N=" + str(p.N))

    while True :    
        outputNextTiling(p)
        p.nextGAMMA()

def goLivret() :
    p = Parameters()
    p.TILINGDIR = "../Pavages/toto"
    p.SAVE, p.SHOW = True, False
    p.N = 5
    p.RECTANGLE = True
    p.R = 61
    p.setGAMMA()
   
    while True :

        for (d, nbl) in [(4,3), (8,6), (15, 8), (30, 16), (60, 33)] :
            p.NBL = nbl
            p.updateDMAX(d)
            outputNextTiling(p)
        
        p.nextGAMMA()


plt.ioff()

 
#go1()
goLivret()
