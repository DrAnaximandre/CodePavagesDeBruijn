import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import math


from parameters import Parameters
from graph import Graph


############### utilities

def inter(a1, b1, c1, a2, b2, c2):
    """ solution of a1 x + b1 y + c1 = 0  and  a2 x + b2 y + c2 = 0 """
    d = a1 * b2 - a2 * b1 
    x = (b1 * c2 - b2 * c1) / d
    y = (a2 * c1 - a1 * c2) / d
    return (x, y)

def get_cos_sin(N):
    """ cos(2 * i * pi / N) for i = 0, ... N-1, and sin idem """
    ANGLE = 2 * math.pi / N
    COS = np.array([np.cos(j * ANGLE) for j in range(N)])
    SIN = np.array([np.sin(j * ANGLE) for j in range(N)])
    return COS, SIN



###################################  tiling computation, following deBruijn paper


# de Bruijn (5.1)
def point(Kvect, COS, SIN, N):
    """ Point associated to [ k_0, ... k_(N-1) ].
        Kvect can be considered as the coordinates of a point in a N dimensional space.
        This function computes the projection of the considered point is the 2-dim ordinary space.
    """
    x, y = 0.0, 0.0
    for j in range(N):
        x += Kvect[j] * COS[j]
        y += Kvect[j] * SIN[j]
    return (x, y)

# de Bruijn (4.4)
def interGrid(r, s, kr, ks, COS, SIN, GAMMA):
    """ Intersection of 2 lines of the pentagrid 
        0 <= r < s < N  and  r,s,kr,ks integers """
    a, b, c = COS[r], SIN[r], GAMMA[r] - kr
    a1, b1, c1 = COS[s], SIN[s], GAMMA[s] - ks
    return inter(a, b, c, a1, b1, c1)

def compute(params: Parameters):
    """ Computes all rhombi determined by N, GAMMA and NBL.
        Returns the rhombi and the corresponding graph of rhombi's vertices and edges
    """

    print('Calcul du pavage, avec les paramètres ' + params.string())
    N = params.N
    NBL = params.NBL
    GAMMA = params.GAMMA.getValue()
    COS, SIN = get_cos_sin(N)

    # coordinates of current rhombus 
    x, y = np.zeros(4), np.zeros(4)
    
    # The index of a vertex could serve later as its 'altitude' for a future 3D display
    # (see de Bruijn paper section 6)
    ind = np.zeros(4)

    #  Kvect is the K of deBruijn's paper, a vector of N integers,
    Kvect = np.zeros(N, dtype=int)

    counter = 0  # count number of computed rhombi

    # for collecting the graph vertices / edges of rhombi
    rhombus_Kvect = np.zeros((4,N), dtype=int)
    graph = Graph(params.ORIENTED)

    # for collecting rhombi
    rhombi = [] # a list    


    # later: compute all combination and TQDM it up
    for r in range(N):  # first grid orientation
        for s in range(r + 1, N):  # second grid orientation
            for kr in range(-NBL, NBL+1):  # line number on r grid
                for ks in range(-NBL, NBL+1):  # line number on s grid

                    # We compute the current rhombus vertices associated to r,s,kr,ks

                    # Pentagrid intersection, de Bruijn (4.4). (xp,yp) is the z_0 of de Bruijn
                    (xp, yp) = interGrid(r, s, kr, ks, COS, SIN, GAMMA)

                    # The following solves a precision problem :
                    # we can prove that (with de Bruijn notation)
                    # K_r(z) = kr when z is on the line (r,kr), hence it is an integer.
                    # Numerical computation of 'ceil' in Kvect below
                    # may incorrectly yield the upper integer.
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
                        ind[j] = sum(Kvect)
                        (x[j], y[j]) = point(Kvect, COS, SIN, N)
                        rhombus_Kvect[j] = Kvect

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

                    # if params.magic > 0:
                    #     if xm < 0 and ym < 0:
                    #         continue



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

                    #display_rhombus(r, s, kr, ks, x, y, ind, params)

                    # Here we collect the graph of connected rhombi vertices.
                    # Kvect, converted to tuple, is convenient as a key in the graph dictionnary.
                    # This is the reason why we keep Kvect in the graph.
                    
                    vs =  [ 0 for i in range(4) ]
                    
                    for i in range(4) :
                        vs[i] = tuple(map(int,rhombus_Kvect[i]))
                        graph.add_vertice(vs[i],x[i],y[i])
                    
                    graph.add_edge(vs[0],vs[1])
                    graph.add_edge(vs[1],vs[2])
                    graph.add_edge(vs[2],vs[3])
                    graph.add_edge(vs[3],vs[0])

                    # We collect the current rhombus by its coordinates
                    rhombi.append((r,s,kr,ks,tuple(ind),tuple(x),tuple(y),d))

                    counter += 1

    print(counter, 'rhombi')
    print(graph.get_order(), 'points (vertices)')
    
    return graph, rhombi

       