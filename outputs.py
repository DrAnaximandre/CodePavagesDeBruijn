from colors import shape_rhombus, kolor
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle

from parameters import Parameters


################################################## draws the rhombus with matplotlib

def mplot(x,y,params) :
    plt.plot(x,y,
             linewidth=params.LINEWIDTH,
             color=params.STROKECOLOR,
             alpha=0.7,
             solid_joinstyle='round',
             solid_capstyle='projecting')   # fin de lignes


def sides(x,y, params):
    xc, yc = np.append(x,x[0]), np.append(y,y[0])
    mplot(xc,yc, params)
    
def fill(x, y, c, alpha=1):
    xy = np.stack((x,y), axis=1)
    #p = Polygon(xy, facecolor=c, edgecolor='black')
    p = Polygon(xy, facecolor=c, alpha = alpha)
    ax = plt.gca()
    ax.add_patch(p)

def line(xA,yA,xB,yB, params) :
    x, y = [xA,xB], [yA,yB]
    mplot(x,y, params)

###################################################

def middle(x1, y1, x2, y2):
    return((x1 + x2) / 2.0, (y1 + y2) / 2.0)

def display_rhombus(r, s, kr, ks, x, y, ind, params):
    xm, ym = sum(x) / 4.0, sum(y) / 4.0
    d = math.sqrt(xm * xm + ym * ym)  # distance from the rhombus center to (0,0)

    # we do not draw the rhombus if it is not in the square or the circle centered in the origin
    # and side or diameter 2*DMAX 
    if params.SQUARE :
        if xm < -params.DMAX or xm > params.DMAX or ym < -params.DMAX or ym > params.DMAX :
            return 0
    else :
        if d > params.DMAX:
            return 0

    def l02():
        line(x[0], y[0], x[2], y[2], params)

    def l13():
        line(x[1], y[1], x[3], y[3], params)

    # draws the rombii sides
    if params.SIDES:
        sides(x,y,params)

    if params.FILLWITHCIRCLE:
        c = kolor(r, s, kr, ks, d, params, x, y)
        std = 2 - d ** 2 / params.DMAX ** 2
        xn, yn = np.random.normal(x, std), np.random.normal(y, std)
        xy = np.stack((xn, yn), axis=1)
        p = Circle(xy.mean(0), radius= np.sqrt(np.max((xy-xy.mean(0))**2)), facecolor=c, alpha=0.9)
        ax = plt.gca()
        ax.add_patch(p)

    elif params.FILL:
        c = kolor(r,s,kr,ks,d, params, x, y)

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
    else:
        pass # no fill

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
            
    return 1