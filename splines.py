import numpy as np
import scipy.interpolate as sinterp
import matplotlib.pyplot as plt

from graph import Graph
import outputs
import tiling
import utils
from parameters import Parameters
from parametersSplines import ParametersSplines
import palettes


def splines(params : Parameters) :

    paramsSplines = params.PARAMS_SPLINES

    graph, rhombs = tiling.compute(params)

    outputs.prepare_display(params)
    graph.display(params)  # decommenter pour visualiser le graphe d'origine (les losanges)

    # construction du nouveau graphe des segments comme quand on dessine pour R=62 (cf outputs)
    # c'est-à-dire des 'pseudo-diagonales' ou des bords de rectangles inscrits
    graphR62 = Graph()

    # ajoute une arete de A à B dans le graphR62
    def arete(xA, yA, KsA, xB, yB, KsB):
        iA = graphR62.add_vertice(tuple(KsA), xA, yA)
        iB = graphR62.add_vertice(tuple(KsB), xB, yB)
        graphR62.add_edge(iA, iB)

    #  construction du nouveau graphe à partir de l'ancien
    print('    Calcul du nouveau graphe')

    #for (r, s, kr, ks, vs, d) in rhombs:
    for (r, s, kr, ks, vs, xs, ys, d) in rhombs:

        #xs = [graph.get_x(vs[i]) for i in range(4)]
        #ys = [graph.get_y(vs[i]) for i in range(4)]

        x01, y01, x12, y12, x23, y23, x30, y30 = utils.middles(xs, ys)
        # les Ks sont indispensables car ce sont les clés pour les entrées dans le graphe
        Ks = np.array([graph.get_K(vs[i]) for i in range(4)])  # de tuple à array

        # en gros, newKs correspond aux milieux des côtés du losange
        # ce sont les clés pour entrer dans le nouveau graphe
        newKs = [Ks[i] + Ks[(i + 1) % 4] for i in range(4)]

        # sh = outputs.shape_rhombus(r, s, params.N)
        sh = outputs.shape_rhombus(r, s, params)
        if sh == 1:  # pseudo-diagonals
            arete(x12, y12, newKs[1], x30, y30, newKs[3])
            arete(x23, y23, newKs[2], x01, y01, newKs[0])
        else:  # side of inner rectangle
            arete(x01, y01, newKs[0], x12, y12, newKs[1])
            arete(x23, y23, newKs[2], x30, y30, newKs[3])


    # print('graphR62 = \n', graphR62)

    # si on veut voir le nouveau graphe, décommenter
    # graphR62.display(params)
    # et les index des sommets
    # graphR62.display_vertices_indexs()

    # on calcule les chemins de ce nouveau graphe,
    # ce sont ses composantes connexes
    print('    Calcul des composantes connexes du nouveau graphe')
    ccs = graphR62.composantes_connexes()

    print('    Il y a ', len(ccs), ' composantes connexes (chemins)')
    maxi = max(len(cc) for cc in ccs)
    # etendue = maxi-mini
    # print(h)
    # unique, counts = np.unique(h, return_counts=True)
    # print(unique,'\n',  counts)


    print('    Calcul et dessin des splines')
    nom_palette = paramsSplines.PALETTE
    params.PALETTE = nom_palette  # pour l'écrire dans le livre (dans le fichier params.txt)
    palette = palettes.get(nom_palette)

    cif = paramsSplines.COLOR_INDEX_FUNCTION

    for cc in ccs:

        """ dessine une composante connexe c'est-à-dire un chemin du graph """

        if paramsSplines.ONLY_PERIODIC :
            periodic = graphR62.exist_edge(cc[0], cc[-1])
            if not periodic: continue
        nbp = len(cc)
        if nbp < paramsSplines.MIN_LENGTH: continue
        color = palette(cif(nbp, maxi))
        display(paramsSplines, cc, graphR62, color, )


    outputs.finalize_display(params)



def display(paramsSplines : ParametersSplines,
            chemin:list[int], graph:Graph, color: tuple[float, float, float, float],
            linewidth: float = 1.0,
            s: float = 1.5, magn:int = 50) :

    """ Calcule et dessine une smoothing spline définie par les points
                     d'un chemin du graphe graph.
                Remarque: si DMAX est grand, les chemins sont
                    très discrétisés et les splines sont quelque peu superflues

        chemin : donné par une liste d'entiers qui sont les index des sommets du graph à approcher

        color : rvb color

        S` est le facteur de lissage (smoothing factor )
           s == 0  ->  interpolating spline = passe par tous les sommets du chemin
           plus s est grand, plus la spline s'éloigne des sommets du chemin
           Une bonne fonction est par exemple : lambda len(chemin) : 0.01 if len(chemin) < 12 else 1.0

        MAGN : la spline est calculée en MAGN*len(chemin) points
            ATTENTION : si MAGN est trop petit on voit la discrétisation
            et pire : elle n'est pas assez fine dans les courbes serrées
    """

    lc = len(chemin)
    if lc <= 3 : return  # au minimum 3 SINON splev PLANTE

    periodic = graph.exist_edge(chemin[0], chemin[-1])
    if periodic : chemin.append(chemin[0])  # indispensable pour dessiner la spline correctement

    xs = np.array([graph.get_x(v) for v in chemin])
    ys = np.array([graph.get_y(v) for v in chemin])

    # `per=True` enforces periodic boundary conditions
    #  tck est utilisé plus bas par splev
    tck, _ = sinterp.splprep([xs, ys], s=paramsSplines.S, per=periodic)

    # ( Parameter values : 0 to 1 )
    u_fine = np.linspace(0, 1, int(paramsSplines.MAGN * lc))
    x_smooth, y_smooth = sinterp.splev(u_fine, tck)
    plt.plot(x_smooth, y_smooth, color=color, linewidth= paramsSplines.LINE_WIDTH)





