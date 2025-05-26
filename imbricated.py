import numpy as np
from parameters import Parameters
import outputs
import gamma as gm
import tiling
import matplotlib.pyplot as plt
import acm_kruskal

N = 8
NUM_IMBRICATED = 3  # Number of imbricated tilings

gamma = gm.MappedGammaParameter(
    N=N,
    initialShift=1.2345,
    functionToMap=lambda s, j: 2 * np.sin(s - (1 + j) / 9) + 0.1 * j / 9 + np.cos(j),
)


DMAXs = [4, 8, 12, 16, 20]  # Maximum degrees for each imbricated tiling


# Parameter definitions for each imbricated tiling
params = []

for dmax in DMAXs:
    params.append(
        Parameters(
            N=N,
            GAMMA=gamma,
            DMAX=dmax,
            BACKGROUND=[0, 0, 0],
            NBL=10,
            STROKECOLOR="w",
            save=False,
            SCALE_LINEWIDTH=dmax*2,
            c=1.2,
        )
    )

# Compute tilings for each parameter set
graphs = []
for p in params:
    graph, _ = tiling.compute(p)
    graphs.append(graph)


# Extract vertex data for each graph
vertex_data = []
for graph in graphs:
    vs = graph.get_vertices()
    xys = [graph.get_xy(v) for v in vs]
    xys = [(round(x, 3), round(y, 3)) for x, y in xys]
    vertex_data.append(xys)

xs = []
ys = []

for xys in vertex_data:
    x_temp, y_temp = zip(*xys)
    xs.append(x_temp)
    ys.append(y_temp)


sx = -4
sy = 4

# Compute edges using acm_kruskal
edges = []
for i in range(len(graphs)):
    if i == 2:
        edges.append(acm_kruskal.compute(graphs[i], [sx, sy], invert_distance=True))
    else:
        edges.append(acm_kruskal.compute(graphs[i], [sx, sy]))

def plot_edges(
    x, y, edges, p, ax, center, bonus=[], offset_color=0.5
):  
    for (i, j) in edges:
        if i in bonus or j in bonus:
            pass
        else:
            xi, xj, yi, yj = x[i], x[j], y[i], y[j]
            outputs.fancy_mplot([xi, xj], [yi, yj], 1, p, ax, center, offset_color)


def find_index(xys1, xys2):
    idx = []
    for i in range(len(xys1)):
        try:
            idx.append(xys2.index(xys1[i]))
        except ValueError:
            pass
    return idx

idxss = [[]]
for i in range(1,len(graphs)):
    idxss.append(find_index(vertex_data[i-1], vertex_data[i]))
    

for i in range(len(graphs)):
    params[i].PREFIX = 2 


fig, ax = outputs.prepare_display(params[-1])  # Use parameters from the second tiling

for i in range(len(graphs)):
    if i%2 == 0:
        plot_edges(xs[i], ys[i], edges[i], params[i], ax, [sx, sy], idxss[i], offset_color=0.054)
 

plt.show()