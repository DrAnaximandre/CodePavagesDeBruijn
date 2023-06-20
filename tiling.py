import matplotlib.pyplot as plt
from pathlib import Path

import numpy as np
import math
import tqdm   # to show computation progress on console

from parameters import Parameters
from outputs import display_rhombus

###################################################  tiling computation following deBruijn paper

def get_cos_sin(N):
    ANGLE = 2 * math.pi / N
    COS = np.array([np.cos(j * ANGLE) for j in range(N)])
    SIN = np.array([np.sin(j * ANGLE) for j in range(N)])
    return COS, SIN

def inter(a1, b1, c1, a2, b2, c2):
    """ solution of a1 x + b1 y + c1 = 0  and  a2 x + b2 y + c2 = 0 """
    d = a1 * b2 - a2 * b1 
    x = (b1 * c2 - b2 * c1) / d
    y = (a2 * c1 - a1 * c2) / d
    return (x, y)

# de Bruijn (4.4)
def interGrid(r, s, kr, ks, COS, SIN, GAMMA):
    """ Intersection of 2 lines of the pentagrid 
        0 <= r < s < N  and  r,s,kr,ks integers """
    a, b, c = COS[r], SIN[r], GAMMA[r] - kr
    a1, b1, c1 = COS[s], SIN[s], GAMMA[s] - ks
    return inter(a, b, c, a1, b1, c1)

# de Bruijn (5.1)
def point(Kvect, COS, SIN, N):
    """ Point associated to [ k_0, ... k_(N-1) ] """
    x, y = 0.0, 0.0
    for j in range(N):
        x += Kvect[j] * COS[j]
        y += Kvect[j] * SIN[j]
    return (x, y)

def tiling(params: Parameters):
    """ Computes (and possibly draws) all rombi determined by N, GAMMA and NBL """
    N = params.N
    NBL = params.NBL
    GAMMA = params.GAMMA.getValue()
    COS, SIN = get_cos_sin(N)

    # coordinates of current rhombus
    x, y = np.zeros(4), np.zeros(4)
    
    # The index of a vertex could serve later as its 'altitude' for a future 3D display
    # (see de Bruijn paper section 6)
    ind = np.zeros(4)

    #  Kvect is the K of deBruijn's paper, a vector of N integers
    Kvect = np.zeros(N, dtype=int)

    counter = 0  # count number of displayed rhombii

    # later: compute all combination and TQDM it up
    for r in range(N):  # first grid orientation
        for s in range(r + 1, N):  # second grid orientation
            for kr in range(-NBL, NBL+1):  # line number on r grid
                for ks in range(-NBL, NBL+1):  # line number on s grid

                    # We compute the current rhombus vertices associated to r,s,kr,ks

                    # Pentagrid intersection, de Bruijn (4.4). (xp,yp) is the z_0 of de Bruijn
                    (xp, yp) = interGrid(r, s, kr, ks, COS, SIN, GAMMA)

                    # The following solves a precision problem : we can prove that (with de Bruijn notation)
                    # K_r(z) = kr when z is on the line (r,kr), hence it is an integer.
                    # Numerical computation of 'ceil' in Kvect below may incorrectly yield the upper integer.
                    # To prevent this we directly reassign Kvect[r] to kr. Idem for ks.
                    # Thanks to Zhao Liang (github pywonderland) for this feature.
 
                    for j in range(N):
                        if j == r :
                            Kvect[r] = kr
                        elif j == s :
                            Kvect[s] = ks
                        else : # de Bruijn (4.3)
                            Kvect[j] = math.ceil(xp * COS[j] + yp * SIN[j] + GAMMA[j])

                    # (4.5) computation of the four values of Kvect corresponding
                    # to the four vertices of the current rhombus

                    def setxyind(j):
                        (x[j], y[j]) = point(Kvect, COS, SIN, N)
                        ind[j] = sum(Kvect)
                        if params.OUTPUT_COORDINATES :
                            pre_setKvect[j] = Kvect

                    # (4.5) computation of the four values

                    setxyind(0)

                    Kvect[r] += 1
                    setxyind(1)

                    Kvect[s] += 1
                    setxyind(2)

                    Kvect[r] -= 1
                    setxyind(3)

                    # here we keep the rhombus or not, according to its distance from origin

                    xm, ym = sum(x) / 4.0, sum(y) / 4.0
                    d = math.sqrt(xm * xm + ym * ym)  # distance from the rhombus center to (0,0)

                    # we do not consider the rhombus
                    # if it is not in the square (or the circle) centered in the origin
                    # and 2*DMAX side (or diameter)
                    if params.SQUARE :
                        if xm < -params.DMAX or xm > params.DMAX\
                          or ym < -params.DMAX or ym > params.DMAX :
                            continue
                    else :
                        if d > params.DMAX:
                            continue

                    display_rhombus(r, s, kr, ks, x, y, ind, params)

                    counter += 1

    print(counter, 'rhombuses')


###################################### main function

def outputTiling(params: Parameters):
    fn = params.filename()

    fig, ax = plt.subplots()
    plt.axis('equal')
    plt.axis('off')

    plt.title(params.title(), fontsize=7, y=0, pad=-20.)
    print(params.string())
    
    # drawing limits
    c = 0.95
    lim = params.DMAX * c
    xmin, xmax, ymin, ymax = -lim, lim, -lim, lim
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    # drawing
    tiling(params)

    # the square line around the picture (hum, not so much elegant, another solution ?)
    b = 0.999
    if params.FRAME and params.SQUARE:
        left, bottom, width, height = -lim*b*1.005, -lim*b, lim*2*b*1.005, lim*2*b*1.00
        p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth=0.5)
        ax.add_patch(p)

    # save first and show after !
    if params.SAVE:
        Path(params.TILINGDIR).mkdir(parents=True, exist_ok=True)
        plt.savefig(fn + '.' + params.SAVE_FORMAT, dpi=300) #, bbox_inches="tight")
    if params.SHOW:
         plt.show()

    plt.close()


