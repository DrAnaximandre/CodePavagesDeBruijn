import matplotlib.pyplot as plt
from time import localtime, strftime
from gamma import MappedGammaParameter
from matplotlib import style


######################################################

WHITE = 'w'
BLACK = 'k'

#plt.rcParams['savefig.facecolor'] = "0.8"
plt.rcParams['figure.figsize'] = 8., 8.    # pour petit ecran


class Parameters(object):

    def __init__(self,
                 GAMMA: MappedGammaParameter = MappedGammaParameter(),
                 N: int = 5,
                 DMAX: int = 8,
                 NBL: int = 6,
                 R: int = 0,
                 SAVE: bool = False,
                 SHOW: bool = True,
                 SAVE_FORMAT: str = 'png',
                 SIDES: bool = True,
                 RECTANGLE: bool = False,
                 DIAGONAL: bool = False,
                 BACKGROUND: str = 'w',
                 STROKECOLOR: str = 'k',
                 COLORING: int = 0,
                 TILINGDIR: str = "../Pavages/toto"):


        
        # Must be 4 or higher
        # Set N = 5 for pentagrids. It works also for 7, 9, 11 ....
        # and even for even numbers
        self.N = N

        # Controls the display shape, see below the SQUARE comment
        # Unit : the length of the rhombus side
        self.DMAX = DMAX

        # Half the number of lines in the pentagrid for a fixed angle.
        self.NBL = NBL

        self.GAMMA = GAMMA
                 
        #self.INITIALSHIFT = 0.03  # should not be integer
        #self.DELTASHIFT = 0.1
                   
        self.SCALE_LINEWIDTH = 8.
        self.LINEWIDTH = self.SCALE_LINEWIDTH / self.DMAX

        self.SAVE = SAVE # save to a file ?
        self.SAVE_FORMAT = SAVE_FORMAT # file format for saving, for example pdf, jpeg, png ...
        self.SHOW = SHOW  # show the tiling on the screen ?

        #=============== overall display shape
        # Let C be the center of a rhombus.
        # If SQUARE == True :
        #   if C is not included in the square centered at the origin (center of screen)
        #   and length 2*DMAX, then the rhombus will not be displayed.
        # If SQUARE == False :
        #   if the distance between C and the origin (center of screen)
        #   is greater than DMAX, then the rhombus will not be displayed.
        self.SQUARE = True

        #============== draws a frame at the limits of drawings
        self.FRAME = True

        ##################### DRAWINGS

        # ---- Controls for drawing rombi
        self.SIDES = SIDES  # draws the sides (contours) ?
        self.DIAGONAL = DIAGONAL # draws a diagonal ?
        self.RECTANGLE = RECTANGLE # draws (part of) rectangle inside the rhombus ?
        self.R = R
        #self.R = 0 #  rectangles and only rectangles
        #self.R = 1 # only opposite sides of rectangles
        #self.R = 2 # "Pentaville" : other sides of rectangles
        #self.R = 3 # pseudo-diagonals (join middle of rhombi sides)
        #self.R = 4 #  # as R=1 or R=2 according to the rhombi shape
        #self.R = 5 # same as R=4 but inverse shapes
        #self.R = 61  # mix rectangle side and pseudo-diags, according to rhombi shape
        #self.R = 62  # like 61, the other way

        # ---- Directory where to write the tilings
        self.TILINGDIR = TILINGDIR


        #=============== COLORS

        self.BACKGROUND = BACKGROUND

        # -------- Different color styles,  see the 'colors' module.
        # -- for filling
        # if False, no filling for shapes
        self.FILL = True
        self.COLORING = COLORING   # different coloring styles (if FILL==True), see the colors module
        # -- for contours
        self.STROKECOLOR = STROKECOLOR


        if self.BACKGROUND == self.STROKECOLOR :
            print("WARNING : BACKGROUND == STROKECOLOR !!!")

        if self.BACKGROUND == BLACK :
            style.use('dark_background')



    def updateDMAX(self, dmax):
        self.DMAX = dmax
        self.LINEWIDTH = self.SCALE_LINEWIDTH / self.DMAX

    def filename(self):
        stts = str(strftime("%Y-%m-%d_%H-%M-%S", localtime()))
        name = self.TILINGDIR + "/deBruijn_" + \
               str(self.N) + '_' + stts + "_" + self.GAMMA.string()
        return name

    def title(self):
        sG = self.GAMMA.stringTex() + ' $d_{max}$=' + str(self.DMAX) + ' #L=' + str(self.NBL)
        if self.RECTANGLE:
            sG += ' R=' + str(self.R)
        if self.DIAGONAL:
            sG += ' D'
        return sG

