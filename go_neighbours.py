
import outputs
from gamma import MappedGammaParameter
from parameters import Parameters
import tiling
from utils import linearPoint
import numpy as np

def go_neighbours(config=None):
    """ For each vertex of the tiling,
        draws a polygon that join, for each edge from the vertex,
        a point on this edge at distance k from the vertex."""
    
   
    if config is None:
        params = {}
        draw_edges = True
        k = 0.333
        N = 7
    else:
        print("Using config file")
        params = config.get('Parameters', {})
        draw_edges = config.get('draw_edges', True)
        print("draw_edges", draw_edges)
        k = config.get('k', 0.333)
        N = config["Parameters"].get('N', 7)


   
    gamma = MappedGammaParameter(
        N=N,
        initialShift=0.23456,
        functionToMap=lambda s, j:  1.85*(np.sin(2*s-(1 + j) / N) +  j /N + np.cos(j))
    )


    params.update({'N':N, 
                    'GAMMA':gamma, 
                    'SCALE_LINEWIDTH':8, 
                    'DMAX':5, 
                    'BACKGROUND':[0.9,  0.882, 0.792], 
                    'NBL':3,
                    'STROKECOLOR':'k',
                    'c': 1.2
                    })
    params = Parameters(**params)
    

    graph, _ = tiling.compute(params)
    
    _, _ = outputs.prepare_display(params)


    color = (0,0,0)
    
    ## draws a polygon around each vertex and colors it
    for v0 in graph.get_vertices() :
        
        (x0,y0) = graph.get_xy(v0)
        nbrs = graph.get_sorted_neighbours(v0)
        xys = [ graph.get_xy(w) for w in nbrs ]
        xysp =  [ linearPoint((x0,y0),xy,k) for xy in xys ]
        xsp,ysp = zip(*xysp)
        outputs.polygon_sides(xsp,ysp,1,params)
        outputs.fill(xsp,ysp,color,1)

    ## draws the central part of each edge
    if draw_edges :
        for (v,w) in graph.get_edges() :
            A = graph.get_xy(v) 
            B = graph.get_xy(w)
            A1 = linearPoint(A,B,k)
            B1 = linearPoint(B,A,k)
            x,y = zip(A1,B1)
            outputs.mplot(x,y,1, params)

        
    outputs.finalize_display(params, close=True)



if __name__ == "__main__":

    print("Running go_neighbours.py")
    go_neighbours()