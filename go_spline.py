import numpy as np

import gamma as gm
import outputs
import tiling
import utils
# from parametersBook import ParametersBook
from parameters import Parameters
#from livre import DMAX_to_NBL
from graph import Graph
import spline
import palettes

# TODO : des morceaux de codes à mettre dans Graph ?

def splines_Livret4D():
    n=7
    dmax = 10
    #gammaLivret4 = gm.MappedGammaParameter(initialGammaValue=[-0.049, -0.058, -0.066, -0.075, -0.083])
    gammaLivret4 = gm.MGPcentralSymetry(n)

    # parametres du pavage support
    params = Parameters(N=n, DMAX=dmax, NBL=6,
                            GAMMA=gammaLivret4,
                            SQUARE = False,
                            SCALE_LINEWIDTH=1, 
                            STROKECOLOR='grey',
                            BACKGROUND='k',
                            SHOW=True,
                            tilingdir='../Results/Splines',
    )

    graph, rhombs = tiling.compute(params)

    outputs.prepare_display(params)
    #graph.display(params)  # decommenter pour visualiser le graphe d'origine (les losanges)

    # le nouveau graphe des segments comme pour R=62 (cf outputs)
    graphR62 = Graph(oriented=True)

    # ajoute une arete de A à B dans le graphR62
    def arete(xA, yA, KsA, xB, yB, KsB) :
        iA = graphR62.add_vertice(tuple(KsA), xA, yA )
        iB = graphR62.add_vertice(tuple(KsB), xB, yB)
        graphR62.add_edge(iA, iB)

    print(len(rhombs[0]))
    #  construction du nouveau graphe à partir de l'ancien
    for (r, s, kr, ks, vs, _, _, _, d) in rhombs:

        xs = [graph.get_x(vs[i]) for i in range(4)]
        ys = [graph.get_y(vs[i]) for i in range(4)]

        x01, y01, x12, y12, x23, y23, x30, y30 = utils.middles(xs, ys)
        # les Ks sont indispensables car ce sont les clés pour les entrées dans le graphe
        Ks = np.array([ graph.get_K(vs[i]) for i in range(4) ])   # de tuple à array

        # en gros, newKs correspond aux milieux des côtés du losange
        # ce sont les clés pour entrer dans le nouveau graphe
        newKs = [ Ks[i] + Ks[(i+1) % 4] for i in range(4)]

        sh = outputs.shape_rhombus(r, s, params.N)
        if sh == 1:  # pseudo-diagonals
            arete(x12, y12, newKs[1], x30, y30, newKs[3])
            arete(x23, y23, newKs[2], x01, y01, newKs[0])
        else:  # side of inner rectangle
            arete(x01, y01, newKs[0], x12, y12, newKs[1])
            arete(x23, y23, newKs[2], x30, y30, newKs[3])

    #print('graphR62 = \n', graphR62)

    # si on veut voir le nouveau graphe
    #graphR62.display(params)
    # et les index des sommets
    # graphR62.display_vertices_indexs()

    ccs = graphR62.composantes_connexes()

    print('Il y a ', len(ccs), ' composantes connexes (chemins)' )
    maxi = max(len(cc) for cc in ccs)
    #etendue = maxi-mini
    #print(h)
    #unique, counts = np.unique(h, return_counts=True)
    #print(unique,'\n',  counts)

    #colormap = CMAP_CUBELIX1(maxi+1)
    #colormap = [ CMAP_TWILIGHT( l / maxi ) for l in range(maxi+1) ]

    for cc in ccs :

        periodic = graphR62.exist_edge(cc[0], cc[-1])
        #if not periodic : break

        nbp = len(cc)
        color = palettes.CUBELIX1(nbp/maxi)

        print(f'{nbp=}   {color=}')
        spline.display(cc, graphR62, color, )

    outputs.finalize_display(params)


splines_Livret4D()