import matplotlib.pyplot as plt
import numpy as np
import math

import tqdm   # un truc pour indiquer à la console l'avancement du calcul

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
def point(k, COS, SIN, N):
    """ Point associated to [ k_0, ... k_(N-1) ] """
    x, y = 0.0, 0.0
    for j in range(N):
        x += k[j] * COS[j]
        y += k[j] * SIN[j]
    return (x, y)

def tiling(params: Parameters):
    """ Computes (and possibly draws) all rombi determined by N, GAMMA and NBL """
    N = params.N
    NBL = params.NBL
    GAMMA = params.GAMMA.getValue()
    COS, SIN = get_cos_sin(N)

    # coordonnees du rhombus courant
    x, y = np.zeros(4), np.zeros(4)
    
    # The index of a vertex could serve as its 'altitude' for a future 3D display
    # (see de Bruijn paper section 6)
    ind = np.zeros(4)
    
    Kvect = np.zeros(N, dtype=np.int)
    pre_setKvect = np.zeros((4,N), dtype=np.int)
    setKvect = set()
    
    counter = 0

    #for r in tqdm.tqdm(range(params.N)):  # first grid orientation
    for r in range(N):  # first grid orientation
        for s in range(r + 1, N):  # second grid orientation
            for kr in range(-NBL, NBL+1):  # line number on r grid
                for ks in range(-NBL, NBL+1):  # line number on s grid

                    # We compute the rhombus vertices associated to r,s,kr,ks

                    # Pentagrid intersection, de Bruijn (4.4). (xp,yp) is the z_0 of de Bruijn 
                    (xp, yp) = interGrid(r, s, kr, ks, COS, SIN, GAMMA)

                    #  Kvect is the K of deBruijn, a vector of N integers
                    # The following seems strange but it works, thanks Zhao Liang (github pywonderland).
                    # This solves a precision problem : we can prove that (with de Bruijn notation)
                    # K_r(z) = kr when z is on the line (r,kr), hence it is an integer.
                    # Numerical computation of 'ceil' in Kvect below may incorrectly yield the upper integer.
                    # To prevent this we directly reassign Kvect[r] to kr. Idem for ks.

                    for j in range(N):
                        if j == r :
                            Kvect[r] = kr
                        elif j == s :
                            Kvect[s] = ks
                        else : # (4.3) 
                            Kvect[j] = math.ceil(xp * COS[j] + yp * SIN[j] + GAMMA[j])
 
                    
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
                        if xm < -params.DMAX or xm > params.DMAX or ym < -params.DMAX or ym > params.DMAX :
                            continue
                    else :
                        if d > params.DMAX:
                            continue

                    # possibility to outputs the set of points coordinates in a file
                    if params.OUTPUT_COORDINATES :    
                        for v in pre_setKvect:
                            setKvect.add(tuple(v))
    
                    display_rhombus(r, s, kr, ks, x, y, ind, params)
                    
                    counter += 1

    print(counter, 'rhombuses')
    
    if params.OUTPUT_COORDINATES :
        nomfich = params.filename_coordinates()
        print('output vertices coordinates in file', nomfich)
        fich = open(nomfich, 'w')
        i = 1
        for s in setKvect:
            (x,y) = point(s,COS,SIN,N)
            fich.write(str(i) + ' ' + str(x) + ' ' + str(y) + '\n')
            i += 1
        
    

######################################

def outputTiling(params: Parameters):

    fn = params.filename()

    fig, ax = plt.subplots()
    plt.axis('equal')
    plt.axis('off')

    plt.title(params.title(), fontsize=8, y=0, pad=-20.)
    # ax.set_ylabel(params.side(), rotation=0,  color="white", loc="bottom")
    # ax.get_xaxis().set_visible(False)
    # ax.yaxis.set_ticklabels([])
    print(params.string())

    # les limites du dessin
    c = 0.95
    lim = params.DMAX * c
    xmin, xmax, ymin, ymax = -lim, lim, -lim, lim
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    # le dessin
    tiling(params)

    # la bordure carrée
    b = 0.999
    if params.FRAME and params.SQUARE:
        left, bottom, width, height = -lim*b*1.005, -lim*b, lim*2*b*1.005, lim*2*b*1.00
        p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth=0.5)
        ax.add_patch(p)


    # save d'abord et show apres !
    if params.SAVE:
        plt.savefig(fn + '.' + params.SAVE_FORMAT, dpi=300) #, bbox_inches="tight")
    if params.SHOW:
         plt.show()

    plt.close()


