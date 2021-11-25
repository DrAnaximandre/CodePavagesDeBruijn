import math
import matplotlib.pyplot as plt


################ Main grid generation parameters

WHITE = 'w'
BLACK = 'k'

def mapR(x, xD, xF, yD, yF) :
    return yD + (yF-yD)/(xF-xD)*(x-xD)

#plt.rcParams['savefig.facecolor'] = "0.8"
#plt.rcParams['figure.figsize'] = 10., 10.
plt.rcParams['figure.figsize'] = 8., 8.    # pour petit ecran


class Parameters(object):

    def __init__(self,
                 N=5,
                 DMAX=8,
                 NBL=6):
        
        # Must be 4 or higher
        # Set N = 5 for pentagrids. It works also for 7, 9, 11 ....
        # and even for even numbers
        self.N = N

        # Controls the display shape, see below the SQUARE comment
        # Unit : the length of the rhombus side
        self.DMAX = DMAX

        # Half the number of lines in the pentagrid for a fixed angle.
        self.NBL = NBL
                 
        self.INITIALSHIFT = 0.03  # should not be integer
        self.DELTASHIFT = 0.1
        
        self.SHIFT = self.INITIALSHIFT
        self.GAMMA = [self.SHIFT] * self.N
                   
        self.SCALE_LINEWIDTH = 15.
        self.LINEWIDTH = self.SCALE_LINEWIDTH / self.DMAX

        self.SAVE = False # save to a pdf file ?
        self.SHOW = True  # show the tiling on the screen ?

        #=============== overall display shape
        # Let C be the center of a rhombus.
        # If SQUARE == True :
        #   if C is not included in the square centered at the origin (center of screen)
        #   and length 2*DMAX, then the rhombus will not be displayed.
        # If SQUARE == False :
        #   if the distance between C and the origin (center of screen)
        #   is greater than DMAX, then the rhombus will not be displayed.
        self.SQUARE = True

        ##################### DRAWINGS

        # ---- Controls for drawing rombi
        self.SIDES = False  # draws the sides (contours) ?
        self.DIAGONAL = False # draws a diagonal ?
        self.RECTANGLE = True # draws (part of) rectangle inside the rhombus ?
        #self.R = 0 #  rectangles and only rectangles
        #self.R = 1   # only opposite sides of rectangles
        #self.R = 2 # Pentaville
        #self.R = 3 # pseudo-diagonals
        #self.R = 4
        self.R = 5

        # ---- Directory where to write the tilings
        self.TILINGDIR = "../Pavages/titi"

        #=============== COLORS


        self.BACKGROUND = WHITE
        #self.BACKGROUND = BLACK

        # -------- Different color styles,  see the 'colors' module.
        # -- for filling
        # if False, no filling for shapes
        self.FILL = False
        self.COLORING = 0   # different coloring styles (if FILL==True), see the colors module
        # -- for contours
        self.STROKECOLOR = BLACK 
        #self.STROKECOLOR = WHITE

        if self.BACKGROUND == self.STROKECOLOR :
            print("WARNING : BACKGROUND == STROKECOLOR !!!")

        if self.BACKGROUND == BLACK :
            mplstyle.use('dark_background')



    def updateDMAX(self, dmax):
        self.DMAX = dmax
        self.LINEWIDTH = self.SCALE_LINEWIDTH / self.DMAX

    ######  GAMMA initialization and behaviour with time.

    def setGAMMA(self):
        # Gives a tiling with perfect central symetry, 
        #  but 'singular' in the deBruijn sense.
        #self.GAMMA = [self.SHIFT] * self.N

        # Tilings could be not exactly symetric
        #self.GAMMA = [self.SHIFT - 0.00085 * j for j in range(self.N)]
        self.GAMMA = [self.SHIFT - 0.05 * j for j in range(self.N)]

        # More or less enforces the deBruijn 'regular' conditions for the tiling
        #   (see the paper, and the 'mathpage' site).
        # Better aspect with small DMAX (i.e. 7) and screen entirely filled.
        #self.GAMMA = [mapR(j, 0, self.N-1, -0.29 + self.SHIFT, 0.19 - self.SHIFT) for j in range(self.N)]
        
        # special "Pentaville" (best for N=5, large DMAX, screen entirely filled) 
        # -- always gives the same tilling ! (does not depend on SHIFT)
        #self.GAMMA = [math.sin(j*math.pi/self.N) for j in range(self.N)]
        #self.GAMMA = [math.sin((j+1)*math.pi/self.N) + j*self.SHIFT/self.N for j in range(self.N)]

        # for livret #2 (avec DIAGONALS) with N=5
        #self.GAMMA = [0.0, 0.486, 0.747, 0.645, 0.180]

        # for livret #3 with R=2 (ancienne valeur, elle a pu changer) pour N=5
        #self.GAMMA = [1.890, 1.885, 1.880, 1.875, 1.870]

    def nextGAMMA(self):
        self.SHIFT -= self.DELTASHIFT
        print(self.SHIFT)
        self.setGAMMA()
     

    def stringGAMMA(self):
        s = "GAMMA="
        for x in self.GAMMA:
            s += ("%+.3f" % x)
        return s

    def stringGAMMAtex(self) :
        g = self.GAMMA
        s = "$\gamma=[" + ("%+.3f" % g[0]) 
        for i in range(1,self.N) :
            s += (",%+.3f" % g[i])
        return s+']$'


