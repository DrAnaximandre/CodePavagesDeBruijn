import numpy as np
from parameters import Parameters
import outputs
import gamma as gm
import tiling
import matplotlib.pyplot as plt
import acm_kruskal

N=8

gamma = gm.MappedGammaParameter(
    N=N,
    initialShift=1.2345,
    functionToMap=lambda s, j:  2*np.sin(s-(1 + j) / 9) + 0.1 * j /9 + np.cos(j)
)

p1 = Parameters(
    N=N,
    GAMMA=gamma,
    DMAX=5,
    BACKGROUND=[0,0,0],
    NBL=5,
    STROKECOLOR='k',
    save=False,
    SCALE_LINEWIDTH=15,
    c=1.2,
)

p2 = Parameters(
    N=N,
    GAMMA=gamma,
    DMAX=14,
    BACKGROUND=[1,1,1],
    NBL=5,
    STROKECOLOR=[0.8,0.1,0.8],
    save=False,
    SCALE_LINEWIDTH=40,
    c=1.2,
    SQUARE=False,
)



graph1, _ = tiling.compute(p1)
graph2, _ = tiling.compute(p2)

vs1 = graph1.get_vertices()
xys1 = [graph1.get_xy(v) for v in vs1]
xys1 = [(round(x, 3), round(y, 3)) for x, y in xys1]
xs1, ys1 = zip(*xys1)

vs2 = graph2.get_vertices()
xys2 = [graph2.get_xy(v) for v in vs2]
xys2 = [(round(x, 3), round(y, 3)) for x, y in xys2]
xs2, ys2 = zip(*xys2)

sx = -4
sy = 4

edges1 = acm_kruskal.compute(graph1, [sx, sy])
edges2 = acm_kruskal.compute(graph2, [sx, sy], invert_distance=True)

def plot_edges(x, 
               y, 
               edges, 
               p, 
               ax, 
               center, 
               bonus= [],
               offset_color=0.5):
    
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

idxss = find_index(xys1, xys2)

fig, ax = outputs.prepare_display(p2)

p2.PREFIX = 3
plot_edges(xs1, ys1, edges1, p1, ax, [sx, sy], offset_color=-0.05)
plot_edges(xs2, ys2, edges2, p2, ax, [sx, sy], idxss, offset_color=0.06)
plt.show()