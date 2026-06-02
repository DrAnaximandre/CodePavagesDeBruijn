
import outputs
from gamma import MappedGammaParameter, MGPNonsense
from parameters import Parameters
import tiling
from utils import linearPoint
import numpy as np
import matplotlib.colors as clrs



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
        print(params)
        draw_edges = config.get('draw_edges', True)
        print("draw_edges", draw_edges)
        k = config.get('k', 0.333)
        N = config["Parameters"].get('N', 7)
        print(config["Parameters"])

    print(N)


   
    gamma = MappedGammaParameter(
        N=N,
        initialShift=0.23456,
        functionToMap=lambda s, j: float(j%3==0) +  1.85*(np.sin(2*s-(1 + j) / N) +  j /N + np.cos(j))
    )

    # gamma = MGPNonsense(N)

    beige = [0.9,  0.882, 0.792]
    params.update({'N':N, 
                    'GAMMA':gamma, 
                    'SCALE_LINEWIDTH':5, 
                    'BACKGROUND':beige, 
                    'STROKECOLOR':'k',
                    'COLORING':11,
                    'SQUARE': False, 
                    'c': 1.5
                    })
   
    params = Parameters(**params)
    

    graph, _ = tiling.compute(params)
    
    _, _ = outputs.prepare_display(params)


    color = (0,0,0)
    color = beige

    vv = graph.get_vertices()
    
    ## draws a polygon around each vertex and colors it
    for v0 in vv:


        (x0,y0) = v0.x, v0.y
        i = v0.index
       
        nbrs = graph.get_sorted_neighbours(i)
    
        xys = [ graph.get_xy(w) for w in nbrs ]
        vv = np.log(np.arange(4,0,-0.05))/np.log(10)


        
        for k in vv:
            xysp =  [ linearPoint((x0,y0),xy,k) for xy in xys ]
            xsp,ysp = zip(*xysp)
            outputs.polygon_sides(xsp,ysp,1,params)
            d = np.mean(np.sqrt(np.array(xysp)**2))
            Ks = np.array( graph.get_K(i))
    
            alpha = np.sin(2 * (Ks[0]* 20 + Ks[1] * 10 + Ks[2] * 15 - d))/2 + 0.5

            outputs.fill(xsp,ysp,color,alpha)
        

    ## draws the central part of each edge
    if draw_edges :
        for (v,w) in graph.get_edges() :
            A = graph.get_xy(v) 
            B = graph.get_xy(w)
            A1 = linearPoint(A,B,k)
            B1 = linearPoint(B,A,k)
            x,y = zip(A1,B1)
            outputs.mplot(x,y,1, params)

        
    fn = outputs.finalize_display(params, close=True)



if __name__ == "__main__":

    print("Running go_neighbours.py")
    go_neighbours()