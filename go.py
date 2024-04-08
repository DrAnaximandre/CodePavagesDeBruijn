import numpy as np
import math
import os

from parameters import Parameters
import tiling
import outputs
import gamma as gm
import utils
import colors
from colors import BLACK, WHITE

#################################### uses all default parameters
def allDefaults():
    outputs.output(Parameters())
    
#################################### a very small tiling
def verySmall():
    outputs.output(Parameters(DMAX=2,NBL=0))

####################################
def colored():
    params = Parameters(N=7)
    graph, rhombi = tiling.compute(params)
    #for c in [0,1,2,3,4,9,10,11,12, 13,14,15,16,17,18,19,23]:
    for c in [0,1,2,3,4,9,10,11,12,13,14,15,19,23]:
        params.COLORING = c
        print('COLORING=', c)
        outputs.output1(graph, rhombi, params)

####################################
def photo_default():
    params = Parameters(N=5, DMAX=30, NBL=15, COLORING=17, SCALE_LINEWIDTH=0)
    graph, rhombi = tiling.compute(params)
    print(f'photo default={params.IMAGEPATH}')
    outputs.output1(graph, rhombi, params)

####################################
def photos():
    imagedir =  "../Photos_input"
    params = Parameters(N=5, DMAX=10, NBL=7, COLORING=17, SCALE_LINEWIDTH=5,
                        SAVE=True, SHOW = False,
                        BACKGROUND = 'k',
                        PREFIX = 2,
                        TILINGDIR = "../Results/Photos_output")
    #params = Parameters(N=5, DMAX=3, NBL=6, COLORING=17, SCALE_LINEWIDTH=0)
    #params.IMAGEDIR = imagedir
    graph, rhombi = tiling.compute(params)
    files = os.listdir(imagedir)
    for f in files :
        print(f)
        params.set_image(imagedir + '/' + f)
        outputs.output1(graph, rhombi, params)

#############################
def rectangles():
    params = Parameters(N=7,SIDES=False,RECTANGLE=True)
    graph, rhombi = tiling.compute(params) 
    outputs.output1(graph, rhombi, params)
    params.BACKGROUND = BLACK
    params.STROKECOLOR = WHITE
    params.COLORING=2
    outputs.output1(graph, rhombi, params)
    
    
###################################### with a fixed and initial GAMMA value

SEQUENCE_LIVRET = [(4,3), (8,6), (15, 8), (30, 16), (60, 33), (100, 55)]

def livret():
    N = 5
    gamma = gm.MappedGammaParameter(
        N=N,  # Size
        initialGammaValue = np.array([-0.260, -0.155, -0.050, 0.055, 0.160]),
    )
    p = Parameters(
        GAMMA=gamma,
        N=N,
        SIDES = False,
        RECTANGLE = True,
        R=62,
        FRAME = True,
        SAVE=True,
        SAVE_FORMAT = 'pdf',
        SHOW=False
    )

    for (d, nbl) in SEQUENCE_LIVRET[:4]:
        p.NBL = nbl
        p.updateDMAX(d)
        outputs.output(p)

            
###################################### with a varying GAMMA value

def livretVar():
    N = 5
    initialshift = 0.03
    gamma = gm.MappedGammaParameter(
        N=N,  
        functionToMap=lambda s, j : s - 0.05 * j
    )
    p = Parameters(
        GAMMA=gamma,
        N=N,
        FRAME = True,
        DIAGONAL = True,
        SIDES = False,
        SHOW = False,
        SAVE=True,
        SAVE_FORMAT = 'pdf'
    )

    for i in range(4):
        for (d, nbl) in SEQUENCE_LIVRET[:4]:
            p.NBL = nbl
            p.updateDMAX(d)
            outputs.output(p)

        gamma.setNextValue()


############################### Polo's demo
def demo(N=7):
    """
    goDemo is a demo of the tiling generator.
    It generates white patterns on a black background.

    """
    gamma = gm.MappedGammaParameter(
        N=N,
        initialShift=1.2345,
        functionToMap=lambda s, j:  2*np.sin(s-(1 + j) / N) + 0.1 * j /N + np.cos(j)/N
    )
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        SIDES=False,
        RECTANGLE=True,
        R=1,
        DMAX=25,
        NBL=25,
        COLORING=2,
        i=0,
        SAVE=True,
        SHOW=False,
        SAVE_FORMAT='pdf',
        TILINGDIR = "../Results/demo",
        BACKGROUND = 'k',
        STROKECOLOR = 'w',
        SCALE_LINEWIDTH = 20
    )
    outputs.output(p)

def Polo3D(N=4, shift=1, i=1234, dmax=5, nbl=5):
    gamma = gm.MappedGammaParameter(
        N=N,
        initialShift=shift,
        functionToMap=lambda s, j : s*np.sin((1+j)/5)) #/(1+j))
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=False,
        R=3,
        DIAGONAL=False,
        SIDES=True,
        COLORING=0,
        BACKGROUND = 'k',
        STROKECOLOR= 'k',
        SAVE=True,
        SHOW=True,
        IMAGEPATH="start/fleurs.jpg",
        DESTRUCTURED=False,
        FISHEYE=False,
        AUGMENTED_COLORS=False,
        TILINGDIR= "../Results/Polo3D",
        QUANTUM_COLOR=False,
        i=i,
    )

    p.magic = shift
    p.NBL = nbl
    p.updateDMAX(dmax)
    outputs.output(p)


######################################
def Polo(N=4):
    """
    Go Polo! Go Polo!
    Generate and save pretty images.
    This is a test function, not a demo.
    """
    gamma = gm.MGPpentavilleVariation(N)
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=False,
        R=4,
        FRAME=False,
        DIAGONAL=False,
        SIDES=False,
        DMAX=20,
        NBL=10,
        COLORING=12,  # 16 uses a photo and "tiles" it, doesn't always work ...
        BACKGROUND = 'k',
        STROKECOLOR= 'w',
        SAVE=True,
        SHOW=True,
        IMAGEPATH="catinspace.png",
        DESTRUCTURED=False,
        FISHEYE=False,
        AUGMENTED_COLORS=False,
        TILINGDIR="../Results/Polo",
        QUANTUM_COLOR=False, # very slow, much AI, consider small images
        i=123,
    )
    outputs.output(p)

def PoloVideo(N=7):
    """
    goPoloVideo is a demo of the tiling generator.
    It generates white patterns on a black background.

    """
    def ftm(k, s, j):
        """
        Function to map.
        """
        g = np.sin(s-(1 + j) / 7) + 0.1 * j /7 + np.cos(j)/7
        if j==0:
            g *= np.cos(k/3)
        elif j==1:
            g += np.cos(k/20)
        elif j==2:
            g *= np.cos(k/5) + np.cos(k/7)
        elif j==4:
            g += 3*np.sin(k/5)
        return g


    gamma = gm.MappedGammaParameter(
        N=5,
        initialShift=1.2345,
        functionToMap = lambda s, j : ftm(N, s, j)
    )
    p = Parameters(
        GAMMA=gamma,
        N=gamma.N,
        RECTANGLE=True,
        SIDES=False,
        R=1,
        DMAX=15,
        NBL=8,
        COLORING=0,
        i=N,
        SAVE=True,
        SHOW=False,
        SAVE_FORMAT='png',
        TILINGDIR="../Results/testf",
        BACKGROUND="k",
        STROKECOLOR="w"
    )
    outputs.output(p)



################################### miscellanous

def centralSymetry() :
    p = Parameters(GAMMA = gm.MGPcentralSymetry())
    outputs.output(p)

def notExactSymetry() :
    p = Parameters(GAMMA = gm.MGPnotExactSymetry())
    outputs.output(p)
 
def DeBruijnRegular(N = 5):
    p = Parameters(
        GAMMA = gm.MGPdeBruijnRegular(N),
        N=N)
    outputs.output(p)

def pentaville() :
    N = 5
    gamma = gm.MGPpentaville(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        NBL = 8,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    outputs.output(p)
 
def pentavilleS() :
    N = 5
    gamma = gm.MGPpentavilleS(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        NBL = 8,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    for i in range(4) :
        outputs.output(p)
        gamma.setNextValue()

        
def pentavilleVariation() :
    N = 5
    gamma = gm.MGPpentavilleVariation(N)
    p = Parameters(
        N = N,
        GAMMA = gamma,
        DMAX = 12,
        NBL = 8,
        SIDES = False,
        RECTANGLE = True,
        R = 2,
        FRAME = True)
    for i in range(4) :
        outputs.output(p)
        gamma.setNextValue()



        
##############################################
##############################################

#    N E W   F E A T U R E S

##############################################
##############################################
    
def neighbours(DMAX=12, NBL=8, N=7):
    """ For each vertex of the tiling,
        draws a polygon that join all its neighbours """
    params = Parameters(N=N,
                        DMAX=DMAX,
                        NBL=NBL,
                        SAVE=True,
                        GAMMA=gm.MGPpentavilleVariation(N),
                        SAVE_FORMAT='png',
                        TITLEREF='neighbours')
    graph, rhombi = tiling.compute(params)

    # note : we dont use rhombi, only graph
    
    outputs.prepare_display(params)
    
    for v in graph.get_vertices() :
        nbrs = graph.get_sorted_neighbours(v)
        xs,ys = zip(*(graph.get_xy(w) for w in nbrs))
        alpha = 1
        outputs.polygon_sides(xs,ys,alpha,params)

    outputs.finalize_display(params)

def neighbours2(k=0.333, DMAX=12, NBL=8, TILINGDIR="../Results/Polo"):
    """ For each vertex of the tiling,
        draws a polygon that join, for each edge from the vertex,
        a point on this edge at distance k from the vertex."""
    N=7

    gamma = gm.MappedGammaParameter(
        N=N,
        initialShift=1.2345,
        functionToMap=lambda s, j: 5 * np.sin(s - (1 + j) / N) + 0.1 * j / N + np.cos(j) / N
    )

    params = Parameters(N=N,DMAX=DMAX, NBL=NBL,SAVE=True,
                        BACKGROUND = BLACK, STROKECOLOR = WHITE,
                        #GAMMA = gm.MGPcentralSymetry(),
                        GAMMA = gamma,
                        SAVE_FORMAT = 'png',
                        SHOW=True,

                        #SQUARE = False,
                        k=k,
                        TITLEREF='neighbours2' + str(k),
                        COLORING=13,
                        SCALE_LINEWIDTH = 8,
                        TILINGDIR=TILINGDIR,
                        #STROKECOLOR = colors.rgb(colors.C3)
                        )
    
    graph, rhombi = tiling.compute(params)

    outputs.prepare_display(params)

    ## draws a polygon around each vertex and colors it
    for v0 in graph.get_vertices() :
        
        (x0,y0) = graph.get_xy(v0)
        nbrs = graph.get_sorted_neighbours(v0)
        xys = [ graph.get_xy(w) for w in nbrs ]
        xysp =  [ utils.linearPoint((x0,y0),xy,k) for xy in xys ]
        xsp,ysp = zip(*xysp)
        outputs.polygon_sides(xsp,ysp,1,params)

        d = math.sqrt(x0*x0 + y0*y0)
        h = utils.mapR(d, 0, params.DMAX, 00, 25)/2 # hue
        h += utils.mapR(d**2, 0, params.DMAX**2, 10, 250)/2 # hue
        s = utils.mapR(d, 0, 100, 80, 100)/2  # saturation
        s += utils.mapR(d**2, 0, 100**2, 40, 100)/2  # saturation
        v = 100 # value = brigthness

        hsv = (h,s,v)
        color = colors.rgb(hsv)
 
        # outputs.fill(xsp,ysp,color,1)

    ## draws the central part of each edge
    for (v,w) in graph.get_edges() :
        A = graph.get_xy(v)
        B = graph.get_xy(w)
        A1 = utils.linearPoint(A,B,k)
        B1 = utils.linearPoint(B,A,k)
        x,y = zip(A1,B1)
        outputs.mplot(x,y,1, params)

    outputs.finalize_display(params)


    
##################################
#    experiments
###################################
import matplotlib.pyplot as plt

def compr(v):
    s = ''
    for n in v :
        s += str(n)
    return s

### test et demo du traitement d'un rhombus particulier
def test():
    params = Parameters(DMAX=2,NBL=0,COLORING=1)
    graph, rhombi = tiling.compute(params)

    ## le 1er sommet du graphe
    v0 = graph.get_vertices()[0]
    print('v0=', v0)

    ## ses coordonnées
    (x0,y0) = graph.get_xy(v0)
    #print('x0,y0)=', (x0,y0))

    nbrs = graph.get_sorted_neighbours(v0)
    #nbrs = graph.get_neighbours(v0)
    print('nbrs=', nbrs)

    outputs.prepare_display(params)

    outputs.rhombi_loop(rhombi,params)

    xys = [ graph.get_xy(v) for v in nbrs ]
    xs,ys = zip(*xys)

    alpha = 1.0   # 1.0 : segments visibles ; 0.0 : invisibles
    outputs.polygon_sides(xs,ys,alpha,params)

    plt.text(x0,y0,'*'+compr(v0))
    for i,v in enumerate(nbrs) :
        (x,y) = graph.get_xy(v)
        plt.text(x,y,str(i)+' '+compr(v))

    outputs.finalize_display(params)


    
