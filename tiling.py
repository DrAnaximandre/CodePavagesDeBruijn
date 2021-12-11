import matplotlib.pyplot as plt
import numpy as np
import math

from parameters import Parameters
from outputs import display_rhombus

def get_cos_sin(params: Parameters):
    ANGLE = 2 * math.pi / params.N
    COS = np.array([np.cos(j * ANGLE) for j in range(params.N)])
    SIN = np.array([np.sin(j * ANGLE) for j in range(params.N)])
    return COS, SIN

def inter(a1, b1, c1, a2, b2, c2):
    """ solution of a1 x + b1 y + c1 = 0  and  a2 x + b2 y + c2 = 0 """
    d = a1 * b2 - a2 * b1 
    x = (b1 * c2 - b2 * c1) / d
    y = (a2 * c1 - a1 * c2) / d
    return (x, y)

# de Bruijn (4.4)
def interGrid(r, s, kr, ks, COS, SIN, params: Parameters):
    """ Intersection of 2 lines of the pentagrid 
        0 <= r < s < N  and  r,s,kr,ks integers """
    a, b, c = COS[r], SIN[r], params.GAMMA[r] - kr
    a1, b1, c1 = COS[s], SIN[s], params.GAMMA[s] - ks
    return inter(a, b, c, a1, b1, c1)

# de Bruijn (5.1)
def f(k, COS, SIN, params: Parameters):
    """ Point associated to [ k_0, ... k_(N-1) ] """
    x, y = 0, 0
    for j in range(params.N):
        x += k[j] * COS[j]
        y += k[j] * SIN[j]
    return (x, y)

def tiling(params: Parameters):

    COS, SIN = get_cos_sin(params)
    """ Computes (and possibly draws) all rombi determined by N, GAMMA and NBL """
    x, y = np.zeros(4), np.zeros(4)
    # The index of a vertex could serve as its 'altitude' for a future 3D display
    # (see de Bruijn paper section 6)
    ind = np.zeros(4)

    for r in range(params.N):  # first grid orientation
        for s in range(r + 1, params.N):  # second grid orientation
            for kr in range(-params.NBL, params.NBL+1):  # line number on r grid
                for ks in range(-params.NBL, params.NBL+1):  # line number on s grid

                    # We compute the rhombus vertices associated to r,s,kr,ks

                    # Pentagrid intersection
                    (xp, yp) = interGrid(r, s, kr, ks, COS, SIN, params)

                    # (4.3)
                    Kvect = np.array([math.ceil(xp * COS[j] + yp * SIN[j] + params.GAMMA[j])
                                      for j in range(params.N)])
                    
                    # (4.5)
                    # The following seems strange but it works, thanks Zhao Liang (github pywonderland).
                    # This solves a precision problem : we can prove that (with de Bruijn notation)
                    # K_r(z) = kr when z is on the line (r,kr), hence it is an integer.
                    # Numerical computation of 'ceil' in Kvect above may incorrectly yield the upper integer.
                    # To prevent this we directly reassign Kvect[r] to kr. Idem for ks.

                    def xyind(j, params):
                        (x[j], y[j]) = f(Kvect, COS, SIN, params)
                        ind[j] = sum(Kvect)

                    Kvect[r], Kvect[s] = kr, ks
                    xyind(0, params)

                    Kvect[r] += 1
                    xyind(1, params)

                    Kvect[s] += 1
                    xyind(2, params)

                    Kvect[r] -= 1
                    xyind(3, params)

                    display_rhombus(r, s, kr, ks, x, y, ind, params)


######################################

def outputNextTiling(params: Parameters):
    fn = params.filename()

    fig, ax = plt.subplots()
    plt.axis('equal')
    plt.axis('off')
    plt.title(params.title(), fontsize=8, y=0, pad=-20.)

    # les limites du dessin
    lim = params.DMAX * 0.93
    xmin, xmax, ymin, ymax = -lim, lim, -lim, lim
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    # la bordure carrée
    if params.FRAME and params.SQUARE:
        left, bottom, width, height = -lim * 1.005, -lim, 2.01 * lim, 2 * lim
        p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth=0.2)
        ax.add_patch(p)

    tiling(params)

    # save d'abord et show apres !
    if params.SAVE:
        plt.savefig(fn + ".pdf", bbox_inches="tight")
    if params.SHOW:
        plt.show()

    plt.close()



