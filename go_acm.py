import numpy as np
import matplotlib.pyplot as plt
from parameters import Parameters
import tiling
import acm_kruskal
import outputs
from gamma import MappedGammaParameter

def glyphs(memory_prefix = 1, 
             offset_boundaries=0.3, 
             offset_n=3,
             ny = 5,
             nx = 7,
             offset_edge=3,
             offset_j=0,
             set_lims=True,
             offset_color=lambda j,i: i**2+np.sqrt(1.5*j),
             NBL=5,
             nsb=False,
             ):


    final_fig, final_ax = plt.subplots(nx,ny-offset_j)
    if nsb:
        final_fig.set_facecolor((1,1,1))
    else:
        final_fig.set_facecolor((0,0,0))

    for i in range(0,nx):

        n = offset_n+i

        gamma = MappedGammaParameter(
            N=n,
            #functionToMap=lambda s, j : 20*np.sin(2*j*np.pi/n) + j**2/n**3 + s**2)
            functionToMap=lambda s, j : j/n  + s**2)
        

        params = Parameters(N=gamma.N, 
                            DMAX=6, 
                            NBL=NBL,
                            GAMMA=gamma,
                            SQUARE=False,
                            SCALE_LINEWIDTH=20,
                            STROKECOLOR="k" if nsb else "w",                          
                            output_format="png")

        if memory_prefix==1:
            params.PREFIX = memory_prefix

        graph, _ = tiling.compute(params)


        vs = graph.get_vertices()
        xys = [graph.get_xy(v) for v in vs]
        xs, ys = zip(*xys)

        for j in range(offset_j,ny):

            final_ax[i,j-offset_j].axis('off')

            edgesAccepted = acm_kruskal.compute(graph, [0,0], invert_distance=False)
            edgesAccepted = edgesAccepted[:int((j+1)*offset_edge**2.1)]

            x_min, x_max = float('inf'), float('-inf')
            y_min, y_max = float('inf'), float('-inf')

            for (t,h) in edgesAccepted:
                xi, xj, yi, yj = xs[t], xs[h], ys[t], ys[h]
                outputs.mplot([xi,xj], [yi,yj], 1 if nsb else 0.8, params, final_ax[i,j-offset_j], center=[nx/2,j/2], offset_color=offset_color(j,i))
                
                x_min = min(x_min, xi, xj)
                x_max = max(x_max, xi, xj)
                y_min = min(y_min, yi, yj)
                y_max = max(y_max, yi, yj)

            final_ax[i,j-offset_j].set_xlim(x_min-offset_boundaries, x_max+offset_boundaries)
            final_ax[i,j-offset_j].set_ylim(y_min-offset_boundaries, y_max+offset_boundaries)

    if set_lims:
        for i in range(nx):
            x_lims = final_ax[i, ny-offset_j-1].get_xlim()
            y_lims = final_ax[i, ny-offset_j-1].get_ylim()
            for j in range(ny-offset_j):
                final_ax[i, j].set_xlim(x_lims)
                final_ax[i, j].set_ylim(y_lims)

    final_fig.set_size_inches(ny-offset_j, nx)
    plt.show()
    fig_name = f'glyphs3_{ny}_nx{nx}_offset_edge{offset_edge}_offset_j{offset_j}_NBL{NBL}.png'
    final_fig.savefig(fig_name, dpi=300)

if __name__ == "__main__":

    glyphs(ny=4, 
           nx=4, 
           offset_edge=2,
           offset_boundaries=0.5,
           offset_j=0, 
           offset_n=3,
           memory_prefix=1, 
           NBL=6, 
           nsb=False,
           offset_color = lambda j,i: 0.5+i/8+j/np.pi)
