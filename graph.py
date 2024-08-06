from collections import OrderedDict

class Graph(object):
    """ This structure stores the graph of all vertices and edges
    of a tiling (rhombi).
    It is specific to this application. """

    def __init__(self):

        #self.vertices = {}  # dictionary. Keys are the 'Kvect' of the vertices.
        # vertices as an ordered dict
        self.vertices = {}
        self.edges = set()

    def add_vertice(self, s, x, y):
        if s not in self.vertices:
            self.vertices[s] = [set(), x, y]  # set() : set of future neighbours

    def add_edge(self, u, v):
        """ add v in the set of u neighbours, and u in the set of v neighbours  """

        self.vertices[u][0].add(v)
        self.vertices[v][0].add(u)
        # add (u,v) or (v,u) in the set of edges (add both ?)
        if u < v:
            self.edges.add((u, v))
        else:
            self.edges.add((v, u))

    def get_xy(self, s):
        v = self.vertices[s]
        return v[1], v[2]

    def get_x(self, s):
        v = self.vertices[s]
        return v[1]

    def get_y(self, s):
        v = self.vertices[s]
        return v[2]

    def exist_edge(self, s, e):
        return e in self.vertices[s]

    def get_edges(self):
        return self.edges

    def get_vertices(self):
        return list(self.vertices.keys())

    def get_order(self):
        return len(self.vertices.keys())

    def get_degree(self, s):
        return len(self.vertices[s])

    def get_neighbours(self, s):
        """ warning : returns a set """
        l = self.vertices[s]
        return l[0]

    def get_sorted_neighbours(self, s):
        """ neighbours sorted by orientation """
        N = len(s)

        def orientation(v):
            """ gives the orientation of the edge s -> v
            For this, we use the specific knowledge that this is an
            edge of a rhombi, computed in tiling.py, and that v is
            a 'Kvect' (see the De Buijn paper).
            In short, from s to v, only one coordinate changes (r),
            by one unit plus or minus.
            The result j corresponds to the orientation PI*j/N,
            with j in the range 0..2*N-1  """
            for r, vr in enumerate(v):
                if vr > s[r]:
                    return 2 * r
                elif vr < s[r]:
                    return (2 * r + N) % (2 * N)
            exit(0)

        return sorted(self.get_neighbours(s), key=orientation)

    def __repr__(self):
        rep = ""
        for s in self.get_vertices():
            rep += f"{s} :\n"
            for t in self.vertice[s]:
                rep += f"   ->{t}\n"
        return rep

    # The main function to construct MST
    # using Kruskal's algorithm

    def mst(self):
        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])

        def union(parent, rank, x, y):
            x_root = find(parent, x)
            y_root = find(parent, y)

            if rank[x_root] < rank[y_root]:
                parent[x_root] = y_root
            elif rank[x_root] > rank[y_root]:
                parent[y_root] = x_root
            else:
                parent[y_root] = x_root
                rank[x_root] += 1

        edges = sorted(list(self.edges), key=lambda x: self.get_distance(x[0], x[1]))

        result_edges = set()
        result_vertices = set()
        parent = {v: v for v in self.get_vertices()}
        rank = {v: 0 for v in self.get_vertices()}

        for edge in edges:
            u, v = edge
            u_root = find(parent, u)
            v_root = find(parent, v)

            if u_root != v_root:
                result_edges.add(edge)
                result_vertices.add(u)
                result_vertices.add(v)
                union(parent, rank, u_root, v_root)


        result_graph = Graph()

        for vertex in result_vertices:
            x, y = self.get_xy(vertex)
            result_graph.add_vertice(vertex, x, y)

        for edge in result_edges:

            result_graph.add_edge(edge[0], edge[1])

        return result_graph

    def get_distance(self, s, e):
        # Add your distance calculation logic here if needed.
        # For now, just return the Euclidean distance between vertices s and e.
        xs, ys = self.get_xy(s)
        xe, ye = self.get_xy(e)
        return ((xe - xs) ** 2 + (ye - ys) ** 2) ** 0.5

    #    def output(self, nomfich) :
#        #print('graph', self)
#        vsl = self.get_vertices()
#        with open(nomfich, 'w+', encoding="utf-8") as f:
#            for i,v in enumerate(vsl) :
#                voisins = [ vsl.index(w) for w in self.get_neighbours(v) ]
#                #print('$',i,v,voisins)
#                json.dump((i,v,voisins), f)
