import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import numpy as np
from pathlib import Path

from parameters import Parameters
import tiling
import graph as gr
from colors import kolor

################################################################
#      main output functions
################################################################

def output(params:Parameters) :

    graph, rhombi = tiling.compute(params)
    return output1(graph, rhombi, params)


def output1(graph:gr.Graph, rhombi, params:Parameters) :

    prepare_display(params)
    
    rhombi_loop(rhombi,params)
    edges_loop(graph,params)

    return finalize_display(params, close=True)


################################################################
#    prepare display
################################################################

def prepare_display(params:Parameters):
    
    fig, ax = plt.subplots()
    plt.axis('equal')
    plt.axis('off')

    #plt.title(params.title(), fontsize=7, y=0, pad=-20.)

    ax.set_ylabel(params.side(), rotation=0,  color="white", loc="bottom")
    ax.get_xaxis().set_visible(False)
    ax.yaxis.set_ticklabels([])
    print(params.string())
    
    fig.set_facecolor(params.BACKGROUND)
    
    lim = params.DMAX * params.c
    xmin, xmax, ymin, ymax = -lim, lim, -lim, lim
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    # a line around the drawing (hum, not so much elegant, another solution ?)
    b = 0.999
    if params.FRAME and params.SQUARE:
        left, bottom, width, height = -lim*b*1.005, -lim*b, lim*2*b*1.005, lim*2*b*1.00
        p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth=0.5)
        ax.add_patch(p)

    return fig, ax
        
################################################################
#    finalize display
################################################################

def finalize_display(params:Parameters, close=False):

    fn = params.filename()
    if not close:
        fn = f'{params.TILINGDIR}/{params.PREFIX:04}'
        params.PREFIX += 1

    
    ########## save first and show after !
    if params.SAVE:
        Path(params.TILINGDIR).mkdir(parents=True, exist_ok=True)
        plt.savefig(fn + '.' + params.SAVE_FORMAT, dpi=300) 

        print("output saved in file " + fn + '.' + params.SAVE_FORMAT)
    if params.SHOW:
         plt.show()
    if close:
        plt.close()
        if params.SAVE:
            return fn + '.' + params.SAVE_FORMAT

    
##############################################################
#    loop over rhombi
##############################################################

def rhombi_loop(rhombi,params):

    # be sure to fill surfaces first,
    # then to draw lines, otherwise lines could not be seen
    
    for (r,s,kr,ks,ind,x,y,d) in rhombi:
        
        c = kolor(r,s,kr,ks,ind,x,y,d,params)
        
        if params.FILLWITHCIRCLE:

            #std = 1# 2 - d ** 2 / params.DMAX ** 2
            #xn, yn = np.random.normal(x, std), np.random.normal(y, std)
            #xy = np.stack((xn, yn), axis=1)

            xy = np.stack((x, y), axis=1)

            p = Circle(
                xy.mean(0),
                radius= 0.4* np.sqrt(
                d**4/params.DMAX**4,
            ),
            facecolor=c,
            edgecolor=np.mean((c,(0,0,0)), axis=0),
            linewidth=1,
            alpha=0.99)
            ax = plt.gca()
            ax.add_patch(p)

        elif params.FILL:
            
            if params.DESTRUCTURED:
                std = 2-d**2/params.DMAX**2
                xn, yn = np.random.normal(x, std), np.random.normal(y,std)
                # xn = np.random.choice(xn,3, False)
                # yn = np.random.choice(yn,3, False)
            elif params.FISHEYE:
                std = params.magic-d**4/params.DMAX**4
                xn, yn = (0.3*x+std *np.mean(x)), (0.33*y+std *np.mean(y))
            else:
                xn, yn = x, y
                
                if params.QUANTUM_COLOR:             
                    inc = params.QUANTUM_COLOR.predict(255*np.array(c).reshape(1,-1))
                    nc = params.QUANTUM_COLOR.cluster_centers_[inc][0]/255
                else:
                    nc = c
                    
                    #       xn = np.concatenate(([0],xn[:3]))
                    #       yn = np.concatenate(([0],yn[:3]))
                    #       xn = xn[:-1]
                    #       yn = yn[:-1]
                fill(xn, yn, nc, alpha = 1)

        if params.RECTANGLE:
            drawer_rectangle(r,s,kr,ks,ind,x,y,d,params)

        if params.DIAGONAL:
            # draws the shortest rombi diagonal, according to
            # the rombus shape (specific for N=5 but works for any N)
        
            sh = shape_rhombus(r, s, params)

            if sh == 2:
                l02(x,y,params)
            elif sh == 1:
                l13(x,y,params)
            else:
                # shortest diagonal ??
                l02(x,y,params)


            
def drawer_rectangle(r,s,kr,ks,ind,x,y,d, params) :
    """ Draws in a rhombus a rectangle (or part of) 
        which vertices are the middles of rombi sides """
    
    x01, y01 = middle(x[0], y[0], x[1], y[1])
    x12, y12 = middle(x[1], y[1], x[2], y[2])
    x23, y23 = middle(x[2], y[2], x[3], y[3])
    x30, y30 = middle(x[0], y[0], x[3], y[3])

    def l01_12():
        line(x01, y01, x12, y12,params)
        
    def l12_23():
        line(x12, y12, x23, y23,params)

    def l23_30():
        line(x23, y23, x30, y30,params)

    def l30_01():
        line(x30, y30, x01, y01, params)

    sh = shape_rhombus(r,s,params)

    if params.R == 0:  # the whole rectangle and only it
        x1,y1 = [x01,x12,x23,x30],[y01,y12,y23,y30]
        polygon_sides(x1,y1,1,params)
            
    elif params.R == 1: # only opposite sides of rectangles
        l01_12()
        l23_30()
        
    elif params.R == 2: # "Pentaville", other sides of rectangles
        l12_23()
        l30_01()
        
    elif params.R == 3:  # pseudo-diagonals (join middle of rombi sides)
        line(x12, y12, x30, y30, params)
        line(x23, y23, x01, y01, params)
        
    elif params.R == 4:  # specific for N=5 but works for any N
        # like R=1 or R=2 according to the rhombi shape
        if sh == 2:
            l01_12()
            l23_30()
        else:
            l12_23()
            l30_01()
            
    elif params.R == 5: # same as R=4 but inverse shapes 
        if sh == 1:
            l01_12()
            l23_30()
        else:
            l12_23()
            l30_01()
             
    elif params.R == 6 : # mix
        if sh == 1: # côté du rectangle
            l01_12()
            l23_30()
        else: # pseudo-diags
            line(x12, y12, x30, y30, params)
            line(x23, y23, x01, y01, params)
            
    elif params.R == 7 : # mix
        if sh == 1 : # pseudo-diags
            line(x12, y12, x30, y30, params)
            line(x23, y23, x01, y01, params)
        else: # side of rectangle
            l01_12()
            l23_30()
    
            
def polygon_sides(x,y,alpha, params):
    xc, yc = np.append(x,x[0]), np.append(y,y[0])
    mplot(xc,yc, alpha, params)
    
    
def fill(x, y, c, alpha):
    xy = np.stack((x,y), axis=1)
    p = Polygon(xy, facecolor=c, alpha=alpha)
    ax = plt.gca()
    ax.add_patch(p)


def fancy_mplot(x,y,alpha,params,ax, center=[0,0],offset_color=0) :

    if hasattr(params, 'PREFIX'):
        # Adjust stroke color based on distance to the center
        X = np.mean(x)
        Y = np.mean(y)

        distance_to_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
        max_distance = params.DMAX * 2
        ratio = np.sqrt(distance_to_center / max_distance)
        ratio = np.clip(ratio, 0.1, 0.99)

        color = (1 - (0.5 + np.cos(offset_color * ratio**3) / 2), 
                 0.5 + np.sin(offset_color * 2 * ratio) / 2, 
                 1 - ratio**2)
    else:
        color = params.STROKECOLOR

    ax.plot(x,y,
                linewidth=params.LINEWIDTH,
                color=color,
                alpha=alpha,
                solid_joinstyle='round',
                solid_capstyle='round')


def mplot(x,y,alpha,params):
 
    plt.plot(x,y,
            linewidth=params.LINEWIDTH,
            color=params.STROKECOLOR,
            alpha=alpha,
            solid_joinstyle='round',
            solid_capstyle='round')



def middle(x1, y1, x2, y2):
    return((x1 + x2) / 2.0, (y1 + y2) / 2.0)

def line(xA,yA,xB,yB, params) :
    x, y = [xA,xB], [yA,yB]
    mplot(x,y, 1, params)

def l02(x,y,params):
    line(x[0], y[0], x[2], y[2], params)

def l13(x,y,params):
    line(x[1], y[1], x[3], y[3], params)


def shape_rhombus(r, s, params):
    """ the shape_rhombus of a rhombus corresponds to its 'thickness'
        and ranges from 1 to floor(N/2) """
    i = s - r
    if i > params.N / 2:
        i = params.N - i
    return i


#################################################
#    loop over edges (sides of rhombi)
#################################################
    
def edges_loop(graph,params):

    if params.SIDES: # draws sides of rhombi
        for (v,w) in graph.get_edges() :
            xA,yA = graph.get_xy(v) 
            xB,yB = graph.get_xy(w) 
            x,y = [xA,xB], [yA,yB]
            mplot(x,y,1,params)
