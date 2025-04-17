from dataclasses import dataclass

@dataclass
class VerticeValue :
    neighbours : set
    x : float
    y : float
    index : int

def orientation(s,t) :
    """ gives the orientation of the edge s -> t
        For this, we use the specific knowledge that this is an
        edge of a rhombi, computed in tiling.py, and that t is
        a 'Kvect' (see the De Buijn paper).
        In short, from s to t, only one coordinate changes (r),
        by one unit plus or minus.
        The result j corresponds to the orientation PI*j/N,
        with j in the range 0..2*N-1  """

    N = len(s)
    for r, tr in enumerate(t) :
        if tr > s[r] :
            return 2*r
        elif tr < s[r] :
            return (2*r + N) % (2*N)
    exit(0)


class Graph :

    """ This structure stores the graph of all vertices and edges
    of a tiling (rhombi).
    It is specific to this application. """
    
    def __init__(self, oriented:bool) :
        self.vertices = {} # dictionary. Keys are the 'Kvect' of the vertices. Values are instances of VerticeValue
        self.edges = set()
        self.n = 0 # number of vertices in the graph
        self.oriented = oriented  # if oriented edges ( a -> b ) or not ( a <-> b )

    def add_vertice(self,s,x,y) :
        if s not in self.vertices :
            self.vertices[s] = VerticeValue(set(), x,y, self.n) 
            self.n += 1

    def add_edge(self, s, e) :
        """ add e in the set of s neighbours, and s in the set of e neighbours  """
        self.vertices[s].neighbours.add(e)
        self.vertices[e].neighbours.add(s)
        # add (s,e) or (e,s) or both in the set of edges depending on oriented
        if ( not (self.oriented)  ) :
             self.edges.add((s,e))
             self.edges.add((e,s))
        else :
            if s < e :
                self.edges.add((s,e))
            else :
                self.edges.add((e,s))

    def get_xy(self,s) :
        v = self.vertices[s]
        return v.x, v.y

    def get_x(self,s) :
        v = self.vertices[s]
        return v.x

    def get_y(self,s) :
        v = self.vertices[s]
        return v.y

    def get_vertice_index(self,s) :
        v = self.vertices[s]
        return v.index

    def exist_edge(self, s, e) :
        """ is there an edge from s to e ? """
        v = self.vertices[s]
        return e in v.neighbours

    def get_edges(self) :
        return self.edges

    def get_vertices(self) :
        return list(self.vertices.keys())

    def get_order(self) :
        return self.n # len(self.vertices.keys())

    def get_degree(self, s) :
        return len(self.vertices[s])

    def get_neighbours(self,s) :
        """ warning : returns a set """
        v = self.vertices[s]
        return v.neighbours


    def get_sorted_neighbours(self,s):
        """ neighbours sorted by orientation 
            This is useful for taking neighbours in order around the vertice s"""

        def f(t) :
            return orientation(s,t)

        return sorted(self.get_neighbours(s), key = f)
        
    def __repr__(self) :
        rep = ""
        for s in self.get_vertices() :
            i = self.get_vertice_index(s)
            rep += f"{s} [{i}]:\n"
            for t in self.get_neighbours(s) :
                j = self.get_vertice_index(t)
                rep += f"   ->{t} [{j}]\n"
        return rep



