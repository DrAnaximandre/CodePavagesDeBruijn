
import outputs
from gamma import MappedGammaParameter, MGPNonsense
from parameters import Parameters
import tiling
from utils import linearPoint
import numpy as np
import matplotlib.colors as clrs
from output_zoomed import output_zoomed
from output_zoomed_portrait import output_zoomed_portrait

def rgb(my_hsv) :
    (h,s,v) = my_hsv
    c = (h/360, s/100, v/100)
    return clrs.hsv_to_rgb(c)


def go_zoomed_neighbours(config=None):
    """ """
    
   
    if config is None:
        params = {}
        draw_edges = True
        k = 0.333
        N = 7
    else:
        params = config.get('Parameters', {})
        draw_edges = config.get('draw_edges', True)
        k = config.get('k', 0.333)
        N = config["Parameters"].get('N', 7)

   
    gamma = MappedGammaParameter(
        N=N,
        initialShift=0.01,
        functionToMap=lambda s, j: float(j%3==0) +  8.85*(np.sin(2*s-(1 + j) / N) +  j /N + np.cos(j))
    )

    # gamma = MGPNonsense(N)

    beige = [0.9,  0.882, 0.792]
    params.update({'N':N, 
                    'GAMMA':gamma, 
                    'BACKGROUND':beige, 
                    'STROKECOLOR':'k',
                    #"BACKGROUND":"k",
                    #'STROKECOLOR':'mediumblue',
                    'COLORING':11,
                    'SQUARE': False, 
                    })

   
    params = Parameters(**params)    

    graph, _ = tiling.compute(params)
    _, _ = outputs.prepare_display(params)
    
    color = [beige,(0,0,0), beige,(0,0,0), beige]
    # color = beige

    vv = graph.get_vertices()
    
    ## draws a polygon around each vertex and colors it
    for v0 in vv:


        (x0,y0) = v0.x, v0.y
        i = v0.index
       
        nbrs = graph.get_sorted_neighbours(i)
    
        xys = [ graph.get_xy(w) for w in nbrs ]
        
        vv = np.linspace(0, 0.4, 5)
        vv = [k]
        vv = np.linspace(0.48, 0.1, 5)
        
        for si, k in enumerate(vv):
            xysp =  [ linearPoint((x0,y0),xy,k) for xy in xys ]
            xsp,ysp = zip(*xysp)
            outputs.polygon_sides(xsp,ysp,1,params)
            d = np.mean(np.sqrt(np.array(xysp)**2))
            Ks = np.array( graph.get_K(i))

        #     # Color eclat
            # h = 200
            # h += 30 * np.sin(Ks[1] - 15*Ks[3])
            # h= h%360
            # sat = 45
            # sat += np.cos((Ks[3] * 20 + Ks[2] * 10 + Ks[4] * 15 - d)) * 25 + np.sin(2 * (Ks[0]* 20 + Ks[1] * 10 + Ks[2] * 15 - d)) * 24
    #         # sat = sat%100
    #         # if sat < 30:
    #         #     sat = 95
    #         # v  = 50 + np.cos((Ks[2] * 20 + Ks[0] * 10 + Ks[4] * 15 - d)) * 24 + np.sin(2 * (Ks[0]* 20 + Ks[1] * 10 + Ks[2] * 15 - d)) * 5
    #         # color =  rgb((h, sat, v))

    # #         # alpha = np.sin(2 * (Ks[0]* 20 + Ks[1] * 10 + Ks[2] * 15 - d))/2 + 0.5
            alpha = 1

            outputs.fill(xsp,ysp,color[si % len(color)],alpha)
        

    # ## draws the central part of each edge
    if draw_edges :
        for (v,w) in graph.get_edges() :
            A = graph.get_xy(v) 
            B = graph.get_xy(w)
            A1 = linearPoint(A,B,vv[0])
            B1 = linearPoint(B,A,vv[0])
            x,y = zip(A1,B1)
            outputs.mplot(x,y,1, params)

        
    fn = outputs.finalize_display(params, close=True)

    # carte postale
    #fn = "tiling_zoomed_cp/000_21_2026-04-17_21-42-06_65_3_GAMMA=+5.016+2.716-0.001-0.630-0.667+2.007+4.937+.png"
    



    output_zoomed(fn, params)
    #output_zoomed_portrait(fn, params)


if __name__ == "__main__":

    print("Running go_neighbours.py")
    go_zoomed_neighbours()