import numpy as np
import scipy.interpolate as sinterp
import matplotlib.pyplot as plt

from graph import Graph

# todo : background ...  en parametres ?
# todo : les splines se croisent dessus/dessous

def display(chemin:list[int], graph:Graph, color: tuple[float, float, float, float],
            linewidth: float = 1.0,
            s: float = 1.5, magn:int = 50) :

    """ Calcule et dessine une smoothing spline définie par les points
                     d'un chemin du graphe graph.
                Remarque: si DMAX est grand, les chemins sont
                    très discrétisés et les splines sont quelque peu superflues

        chemin : donné par une liste d'entiers qui sont les index des sommets du graph à approcher

        color : rvb color

        s` est le facteur de lissage (smoothing factor )
           s == 0  ->  interpolating spline = passe par tous les sommets du chemin
           plus s est grand, plus la spline s'éloigne des sommets du chemin
           Une bonne fonction est par exemple : lambda len(chemin) : 0.01 if len(chemin) < 12 else 1.0

        magn : la spline est calculée en magn*len(chemin) points
            ATTENTION : si magn est trop petit on voit la discrétisation
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
    tck, _ = sinterp.splprep([xs, ys], s=s, per=periodic)

    # ( Parameter values : 0 to 1 )
    u_fine = np.linspace(0, 1, int(magn * lc))
    x_smooth, y_smooth = sinterp.splev(u_fine, tck)
    plt.plot(x_smooth, y_smooth, color=color, linewidth= linewidth)



