
from colors import shape_rhombus, kolor
import math

import matplotlib.pyplot as plt

import numpy as np
from matplotlib.patches import Polygon



################################################## draws the rhombus with matplotlib

def mplot(x,y,params) :
    plt.plot(x,y,
             linewidth=params.LINEWIDTH,
             color=params.STROKECOLOR,
             solid_joinstyle='round',
             solid_capstyle='round')

def sides(x,y, params) :
    xc, yc = np.append(x,x[0]), np.append(y,y[0])
    mplot(xc,yc, params)
    
def fill(x, y, c) :
    xy = np.stack((x,y), axis=1)
    #p = Polygon(xy, facecolor=c, edgecolor='black')
    p = Polygon(xy, facecolor=c)
    ax = plt.gca()
    ax.add_patch(p)

def line(xA,yA,xB,yB, params) :
    x, y = [xA,xB], [yA,yB]
    mplot(x,y, params)

###################################################

def middle(x1, y1, x2, y2):
    return((x1 + x2) / 2, (y1 + y2) / 2)

def display_rhombus(r, s, kr, ks, x, y, ind, params):
    xm, ym = sum(x) / 4.0, sum(y) / 4.0
    d = math.sqrt(xm * xm + ym * ym)  # distance from the rhombus center to (0,0)

    # we do not draw the rhombus if it is not in the square or the circle centered in the origin
    # and side or diameter 2*DMAX 
    if params.SQUARE :
        if xm < -params.DMAX or xm > params.DMAX or ym < -params.DMAX or ym > params.DMAX :
            return
    else :
        if d > params.DMAX:
            return

    def l02():
        line(x[0], y[0], x[2], y[2], params)

    def l13():
        line(x[1], y[1], x[3], y[3], params)

    # draws the rombii sides
    if params.SIDES:
        sides(x,y,params)

    if params.FILL :
        c = kolor(r,s,kr,ks,d, params)
        fill(x, y, c)

    # draws the shortest rombi diagonal, according to
    # the rombus shape (specific for N=5 but works for any N)
    if params.DIAGONAL:
        sh = shape_rhombus(r, s, params)
        if sh == 2:
            l02()
        if sh == 1:
            l13()

    # rectangle (or part of) which vertices are the middles of rombi sides
    if params.RECTANGLE:

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

        if params.R == 0:  # the whole rectangle 
            x1,y1 = [x01,x12,x23,x30],[y01,y12,y23,y30]
            sides(x1,y1,params)
            if False :
                c = kolor(params.COLORING,r,s,kr,ks,d)
                fill(x1, y1, c)

        elif params.R == 1: # only opposite sides of rectangles
            l01_12()
            l23_30()

        elif params.R == 2: # Pentaville, other sides of rectangles
            l12_23()
            l30_01()

        elif params.R == 3:  # pseudo-diagonals (join middle of rombi sides)
            line(x12, y12, x30, y30, params)
            line(x23, y23, x01, y01, params)

        elif params.R == 4:  # specific for N=5 but works for any N
                             # as R=1 or R=2 according to the rhombi shape
            sh = shape_rhombus(r, s, params)
            if sh == 2:
                l01_12()
                l23_30()
            else:
                l12_23()
                l30_01()

        elif params.R == 5: # same as R=4 but inverse shapes 
            sh = shape_rhombus(r, s, params)
            if sh == 1:
                l01_12()
                l23_30()
            else:
                l12_23()
                l30_01()
                
        elif params.R == 61 : # mélange  
            sh = shape_rhombus(r, s, params)
            if sh == 1: # côté du rectangle
                l01_12() 
                l23_30()
            else: # pseudo-diags
                line(x12, y12, x30, y30, params)
                line(x23, y23, x01, y01, params)

        elif params.R == 62 : # mélange  
            sh = shape_rhombus(r, s, params)
            if sh == 1 :
                # pseudo-diags
                line(x12, y12, x30, y30, params)
                line(x23, y23, x01, y01, params)
            else: # côté du rectangle
                l01_12() 
                l23_30()
            
