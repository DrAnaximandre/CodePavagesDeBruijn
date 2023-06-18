from pathlib import Path
import inspect
import matplotlib.pyplot as plt
from time import localtime, strftime
from matplotlib import style
from PIL import Image
import numpy as np

from gamma import MappedGammaParameter
from sklearn.cluster import KMeans

######################################################

WHITE = 'w'
BLACK = 'k'

# plt.rcParams['savefig.facecolor'] = "0.8"
plt.rcParams['figure.figsize'] = 8., 8.  # pour petit ecran


class Parameters(object):

    def __init__(self,
                 # GAMMA actual value defined later because of N dependancy
                 GAMMA: MappedGammaParameter = None, 
                 N: int = 5,
                 DMAX: int = 8,
                 NBL: int = 5,
                 R: int = 0,
                 SAVE: bool = False,
                 SHOW: bool = True,
                 SAVE_FORMAT: str = 'png',
                 SQUARE: bool = True,
                 FRAME: bool = False,
                 SIDES: bool = True,
                 RECTANGLE: bool = False,
                 DIAGONAL: bool = False,
                 BACKGROUND: str = 'w',
                 STROKECOLOR: str = 'k',
                 COLORING: int = 0,
                 DESTRUCTURED: bool = False,  # Should noise be applied to the coordinates of the rhombi
                 FISHEYE: bool = False,  # another kind of transformation
                 AUGMENTED_COLORS: bool = False,  # Should the colors be tilted a bit
                 IMAGEPATH: str = "mokos.jpg",  # used only for coloring 16, 17, 18
                 QUANTUM_COLOR: bool = False,  # should color be quantized
                 TILINGDIR: str = "../Pavages/DefaultTilingDir",
                 i: int = 0,
                 # to output coordinates of all vertices in a special file
                 OUTPUT_COORDINATES: bool = False,
                 FILENAME_COORDINATES:str = "../../ACM/Data/pavage_coords.txt",
                 SCALE_LINEWIDTH: int= 8):


        
        # Must be 4 or higher
        # Set N = 5 for pentagrids. It works also for 7, 9, 11 ....
        # and even for even numbers
        self.N = N

        # Controls the display shape, see below the SQUARE comment
        # Unit : the length of the rhombus side
        self.DMAX = DMAX

        # Half the number of lines in the pentagrid for a fixed angle.
        self.NBL = NBL

        
        self.GAMMA = GAMMA if GAMMA else MappedGammaParameter(N=N)

        # self.INITIALSHIFT = 0.03  # should not be integer
        # self.DELTASHIFT = 0.1

        self.SCALE_LINEWIDTH = SCALE_LINEWIDTH
        self.LINEWIDTH = self.SCALE_LINEWIDTH / self.DMAX

        self.SAVE = SAVE  # save to a file ?
        self.SAVE_FORMAT = SAVE_FORMAT  # file format for saving, for example pdf, jpeg, png ...
        self.SHOW = SHOW  # show the tiling on the screen ?

        # =============== overall display shape
        # Let C be the center of a rhombus.
        # If SQUARE == True :
        #   if C is not included in the square centered at the origin (center of screen)
        #   and length 2*DMAX, then the rhombus will not be displayed.
        # If SQUARE == False :
        #   if the distance between C and the origin (center of screen)
        #   is greater than DMAX, then the rhombus will not be displayed.
        self.SQUARE = SQUARE

        # ============== draws a frame at the limits of drawings
        self.FRAME = FRAME

        ##################### DRAWINGS

        # ---- Controls for drawing rombi
        self.SIDES = SIDES  # draws the sides (contours) ?
        self.DIAGONAL = DIAGONAL  # draws a diagonal ?
        self.RECTANGLE = RECTANGLE  # draws (part of) rectangle inside the rhombus ?
        self.R = R
        # self.R = 0 #  rectangles and only rectangles
        # self.R = 1 # only opposite sides of rectangles
        # self.R = 2 # "Pentaville" : other sides of rectangles
        # self.R = 3 # pseudo-diagonals (join middle of rhombi sides)
        # self.R = 4 #  # as R=1 or R=2 according to the rhombi shape
        # self.R = 5 # same as R=4 but inverse shapes
        # self.R = 61  # mix rectangle side and pseudo-diags, according to rhombi shape
        # self.R = 62  # like 61, the other way

        # ---- Directory where to write the tilings
        self.TILINGDIR = TILINGDIR
        # create the directory
        Path(self.TILINGDIR).mkdir(parents=True, exist_ok=True)

        # =============== COLORS

        self.BACKGROUND = BACKGROUND

        # -------- Different color styles,  see the 'colors' module.
        # -- for filling
        # if False, no filling for shapes
        self.FILL = True
        self.COLORING = COLORING  # different coloring styles (if FILL==True), see the colors module
        # -- for contours
        self.STROKECOLOR = STROKECOLOR

        self.IMAGEPATH = IMAGEPATH
        self.QUANTUM_COLOR = QUANTUM_COLOR

        if self.COLORING in [16,17,18]:
            # very crude, can be demanding for the CPU if the input image is large

            img = Image.open(self.IMAGEPATH)
            img.load()
            # passe-passe pour loader l'image dans le bon sens
            self.image = np.asarray(img, dtype="int32")
            self.image = np.swapaxes(self.image, 0, 1)
            self.image = np.flip(self.image, 1)
            X = self.image.reshape(self.image.shape[0] * self.image.shape[1], self.image.shape[2])
            # resize si trop grand
            print("fitting kmeans")
            if self.QUANTUM_COLOR:
                color_model = KMeans(n_clusters=15,
                                     random_state=0,
                                     max_iter=100,
                                     init = 'random',
                                     tol=1e-1).fit(X) # Todo, parameterise the number of clusters
                self.QUANTUM_COLOR = color_model
        else:
            if self.QUANTUM_COLOR:
                print('inappropriate parameters, overriding QC ')
                self.QUANTUM_COLOR = False

        self.DESTRUCTURED = DESTRUCTURED
        self.FISHEYE = FISHEYE
        self.AUGMENTED_COLORS = AUGMENTED_COLORS

        self.magic = 0.5
        self.i = i
        self.FILLWITHCIRCLE = False

        # if self.BACKGROUND == self.STROKECOLOR :
        #     print("WARNING : BACKGROUND == STROKECOLOR !!!")

        if self.BACKGROUND == BLACK:
            style.use('dark_background')

        self.OUTPUT_COORDINATES = OUTPUT_COORDINATES
        self.FILENAME_COORDINATES = FILENAME_COORDINATES

    def side(self):
        fn = self.filename()
        return "\n".join([chr(ord(ch) + 2) for ch in fn])



    def updateDMAX(self, dmax):
        self.DMAX = dmax
        self.LINEWIDTH = self.SCALE_LINEWIDTH / self.DMAX

    def filename(self):
        stts = str(strftime("%Y-%m-%d_%H-%M-%S", localtime()))
        name = f"{self.TILINGDIR}/{self.i:03}_{self.N}_{stts}_{self.DMAX}_{self.NBL}_{self.GAMMA.string()}"
        name = name[:100]
        return name

    def title(self):
        sG = "\n\n\n\n\n" + str(self.N) + ' $d_{max}$=' + str(self.DMAX) + ' i=' + str(self.i)
        if self.RECTANGLE:
            sG += ' R=' + str(self.R)
        if self.DIAGONAL:
            sG += ' D'

        sG += self.GAMMA.string()[:50]

        sG += f"\n quantum = {self.QUANTUM_COLOR}"

        # the code that is in the lambda called functionToMap is displayed here
        sG += f" {inspect.getsourcelines(self.GAMMA.functionToMap)[0][0]}"
        return sG

    def string(self):
        sG = self.GAMMA.string() + ' DMAX=' + str(self.DMAX) + ' NBL=' + str(self.NBL)
        if self.RECTANGLE:
            sG += ' R=' + str(self.R)
        if self.DIAGONAL:
            sG += ' D'
        return sG

