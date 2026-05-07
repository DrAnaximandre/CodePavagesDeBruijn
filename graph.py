# new implementation

import math
from dataclasses import dataclass
import matplotlib.pyplot as plt

from parameters import Parameters



@dataclass
class VerticeValue:
    K: tuple          # integer coordinates in Z^N, key of the dictionary of vertices
    neighbours: set[int]
    x: float    # xs coordinate in R^2
    y: float    # y coordinate in R^2
    # ind: int   # 'index' of a vertice (see de Bruijn section 6), possible future use
    index: int   # index of the vertice in the vertice list


class Graph:
    """ 
    This structure stores the graph of all vertices and edges of a tiling.
    The graph is non oriented, that is (i,j) stands for  i <-> j
    It is not a general graph implementation, it is specific to this application.
    """

    # ========= How variables are named :
    # u, v :  VerticeValue
    # K : tuple of int, K of a vertice (see de Bruijn paper)
    # i, j : int, index of vertices in self.verticeList

    def __init__(self):
        self.Kdict = {}  # dictionary, keys are K of vertices, values are indices (ints)
        self.verticeList = []  # list of VerticeValue
        self.edges = set()  # set of edges, an edge is a couple of vertices index
        self.n = 0  # number of vertices in the graph

    def add_vertice(self, K: tuple, x: float, y: float) -> int :
        """
            K is the K of the vertice to be added in the graph, if not already present.
            returns the vertice index (int)
        """
        if K in self.Kdict:
            return self.Kdict[K]
        else:
            i = self.n
            self.Kdict[K] = i
            v = VerticeValue(K, set(), x, y, i)
            self.verticeList.append(v)
            self.n += 1
            return i

    def add_edge(self, i: int, j: int):
        """ 
            i and j are index of vertices.
            Add i in the set of j neighbours, and j in the set of i neighbours
            if i<j , add (i,j) in the set of edges, else  add(j,i)
        """
        self.verticeList[i].neighbours.add(j)
        self.verticeList[j].neighbours.add(i)
        if i < j:
            self.edges.add((i, j))
        else:
            self.edges.add((j, i))

    def get_K(self, i: int):
        v = self.verticeList[i]
        return v.K

    def get_x(self, i: int):
        v = self.verticeList[i]
        return v.x

    def get_y(self, i: int):
        v = self.verticeList[i]
        return v.y

    def get_xy(self, i: int):
        v = self.verticeList[i]
        return v.x, v.y

    def get_xsys(self):
        xs = [v.x for v in self.verticeList]
        ys = [v.y for v in self.verticeList]
        return xs, ys

    def exist_edge(self, i: int, j: int):
        """ is there an edge from i to j ? """
        v = self.verticeList[i]
        return j in v.neighbours

    def get_edges(self):
        return self.edges

    def get_vertices(self):
        return self.verticeList

    def get_order(self):
        return self.n

    def get_degree(self, i: int):
        return len(self.verticeList[i].neighbours)

    def get_neighbours(self, i: int):
        """
            WARNING : returns a set
        """
        
        v = self.verticeList[i]
        return v.neighbours

    def get_sorted_neighbours(self, i: int):
        """
            neighbours sorted by orientation
            This is useful for taking neighbours anti-clockwise around a vertice
        """
        
        return sorted(self.get_neighbours(i), key=lambda j: self.orientation(i, j))

    def distance(self, i: int, j: int):
        v = self.verticeList[i]
        w = self.verticeList[j]
        dx = v.x - w.x
        dy = v.y - w.y
        d2 = dx * dx + dy * dy
        d = math.sqrt(d2)
        return d

    def __repr__(self):
        rep = ""
        for i in range(self.n):
            rep += f"{self.get_vertices()[i]}\n"
        return rep

    def orientation(self, i: int, j: int):
        """ 
            Gives the orientation of the *oriented* edge i -> j
            First we recover the 'K's of i and j (see the de Bruijn paper),
            respectively K_i and K_j.
            Then, we use the specific knowledge that i -> j is an
            edge of a rhombus, computed in tiling.py
            In short, from K_i to K_j, only one coordinate changes (r),
            by one unit plus or minus.
            The result j corresponds to the orientation PI*j/N,
            with j in the range 0..2*N-1
        """
        K_i = self.get_K(i)
        K_j = self.get_K(j)
        N = len(K_i)
        for r, tr in enumerate(K_j):
            if tr > K_i[r]:
                return 2 * r
            elif tr < K_i[r]:
                return (2 * r + N) % (2 * N)
        exit(1)


    def composantes_connexes(self):
        """ Retourne les composantes connexes du graphe
            sous forme de liste de liste d'indexs de sommets.
            Algorithme Depth First Search
        """
        ccs = []  # composantes
        m = [False] * self.n  # marques = Points rencontrées
        vs = list(range(self.n))
        # le tri qui suit permet de traiter en premier les sommets près des bords
        # (qui n'ont qu'un (ou peu) de voisins). Grace à la DFS, les sommets
        # des composantes sont triées dans l'ordre du parcours quand elles
        # sont réduites à des chemins singuliers (pour splines.py)
        vs.sort(key=lambda v: self.get_degree(v))
        for v in vs :
            if not m[v]:
                cc = [v]
                m[v] = True
                pile = list(self.get_neighbours(v))
                while pile:
                    w = pile.pop()
                    if not m[w]:
                        cc.append(w)
                        m[w] = True
                        pile += self.get_neighbours(w)
                ccs.append(cc)
        return ccs




        ###############################

    def display(self, params : Parameters):
        from outputs import mplot
        for (i, j) in self.get_edges():
            xA, yA = self.get_xy(i)
            xB, yB = self.get_xy(j)
            xs, ys = [xA, xB], [yA, yB]
            mplot(xs, ys, 1, params)


    def display_vertices_indexs(self):
    #  display a 'x' at each vertice and its index
        for index in range(self.get_order()):
            (x, y) = self.get_xy(index)
            plt.plot(x, y, 'x', color='k')
            plt.text(x, y, str(index), color='green', fontsize='small', )

