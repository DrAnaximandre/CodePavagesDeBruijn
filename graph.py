class Graph(object) :

    """ This structure stores the graph of all vertices and edges
    of a tiling (rhombi).
    It is specific to this application. """
    
    def __init__(self) :
        self.vertices = {} # dictionary. Keys are the 'Kvect' of the vertices.
        self.edges = set()

    def add_vertice(self,s,x,y) :
        if s not in self.vertices :
            self.vertices[s] = [set(), x,y] # set() : set of future neighbours

    def add_edge(self, s, e) :
        """ add e in the set of s neighbours, and s in the set of e neighbours  """
        self.vertices[s][0].add(e)
        self.vertices[e][0].add(s)
        # add (s,e) or (e,s) in the set of edges (add both ?)
        if s < e :
            self.edges.add((s,e))
        else :
            self.edges.add((e,s))

    def get_xy(self,s) :
        v = self.vertices[s]
        return v[1],v[2]

    def get_x(self,s) :
        v = self.vertices[s]
        return v[1]

    def get_y(self,s) :
        v = self.vertices[s]
        return v[2]

    def exist_edge(self, s, e) :
        return  e in self.vertices[s]

    def get_edges(self) :
        return self.edges

    def get_vertices(self) :
        return list(self.vertices.keys())

    def get_order(self) :
        return len(self.vertices.keys())

    def get_degree(self, s) :
        return len(self.vertices[s])

    def get_neighbours(self,s) :
        """ warning : returns a set """
        l = self.vertices[s]
        return l[0]

    def get_sorted_neighbours(self,s):
        """ neighbours sorted by orientation """
        N = len(s)
        def orientation(v) :
            """ gives the orientation of the edge s -> v
            For this, we use the specific knowledge that this is an
            edge of a rhombi, computed in tiling.py, and that v is
            a 'Kvect' (see the De Buijn paper).
            In short, from s to v, only one coordinate changes (r),
            by one unit plus or minus.
            The result j corresponds to the orientation PI*j/N,
            with j in the range 0..2*N-1  """
            for r, vr in enumerate(v) :
                if vr > s[r] :
                    return 2*r
                elif vr < s[r] :
                    return (2*r + N) % (2*N)
            exit(0)
        return sorted(self.get_neighbours(s), key = orientation)
        
    def __repr__(self) :
        rep = ""
        for s in self.get_vertices() :
            rep += f"{s} :\n"
            for t in self.vertice[s] :
                rep += f"   ->{t}\n"
        return rep
