import hashlib
import json
from dataclasses import dataclass
from functools import partial

import matplotlib.pyplot as plt
import numpy as np

import acm_kruskal
import outputs
import tiling
from gamma import MappedGammaParameter
from parameters import Parameters


def default_offset_color(i,j):
    return i**2+np.sqrt(1.5*j)

def alternative_offset_color(i,j):
    return 0.7+j**2+np.sqrt(i)

def default_functionToMapN(s, j, n):
    return j/n + s**2

@dataclass
class GlyphsColorsParameters:
    offset_color: callable=default_offset_color
    colored_edges: bool = True
    white_bg: bool = False
    center: tuple = (0,0)

@dataclass
class GlyphsFigureParameters:
    offset_boundaries: float = 0.3
    offset_n: int = 3
    nx: int = 7
    ny: int = 5
    offset_j: int = 0
    offset_edge: int = 3
    set_lims: bool = True

@dataclass
class GlyphsParametersParameters:
    NBL: int = 5
    functionToMapN: callable=default_functionToMapN
    SQUARE: bool = True
    SCALE_LINEWIDTH: int = 20
    DMAX: int = 6

@dataclass
class GlyphsParameters:
    cp: GlyphsColorsParameters
    fp: GlyphsFigureParameters
    pp: GlyphsParametersParameters


    def hash_name(self):
        """generate a hash name for the parameters"""
        
        def serialize_callable(obj):
            """serialize a callable object 
            note that the lambda functions will all be called lambda"""
            if callable(obj):
                return obj.__name__
            return obj
         
        params_dict = {
            "cp": self.cp.__dict__,
            "fp": self.fp.__dict__,
            "pp": self.pp.__dict__
        }

        params_str = json.dumps(params_dict, default=serialize_callable, sort_keys=True)
        hash = hashlib.md5(params_str.encode('utf-8')).hexdigest()
        print(hash)

        return hash

def create_figure(fp: GlyphsFigureParameters):
    final_fig, final_ax = plt.subplots(fp.nx,fp.ny-fp.offset_j)
    return final_fig, final_ax


def set_background_color(final_fig, cp: GlyphsColorsParameters):
    if cp.white_bg:
        final_fig.set_facecolor((1,1,1))
    else:
        final_fig.set_facecolor((0,0,0))


def get_gamma(n, pp: GlyphsParametersParameters):
    return MappedGammaParameter(
        N=n,
        functionToMap=partial(pp.functionToMapN, n=n)
    )


def get_parameters(n, pp: GlyphsParametersParameters):
    return Parameters(N=n, 
                    DMAX=pp.DMAX, 
                    NBL=pp.NBL,
                    GAMMA=get_gamma(n, pp),
                    SQUARE=pp.SQUARE,
                    SCALE_LINEWIDTH=pp.SCALE_LINEWIDTH,                         
                    output_format="png")


def change_color(params, cp: GlyphsColorsParameters):
     params.STROKECOLOR="k" if cp.white_bg else "w"

def set_prefix(params, cp: GlyphsColorsParameters):
    if cp.colored_edges:
        params.PREFIX = 1

def get_xs_ys(graph):
    vs = graph.get_vertices()
    xys = [graph.get_xy(v) for v in vs]
    xs, ys = zip(*xys)
    return xs, ys

def update_xy_limits(x_min, x_max, y_min, y_max, xi, xj, yi, yj):
    x_min = min(x_min, xi, xj)
    x_max = max(x_max, xi, xj)
    y_min = min(y_min, yi, yj)
    y_max = max(y_max, yi, yj)
    return x_min, x_max, y_min, y_max


def plot_one_glyph(ax, edges_accepted_local, xs, ys, gp, params, oc):

    x_min, x_max = float('inf'), float('-inf')
    y_min, y_max = float('inf'), float('-inf')
    
    for (t,h) in edges_accepted_local:
        xi, xj, yi, yj = xs[t], xs[h], ys[t], ys[h]
        outputs.fancy_mplot([xi,xj], 
                            [yi,yj],
                            alpha=1 if gp.cp.white_bg else 0.8, 
                            params=params, 
                            ax=ax, 
                            center=gp.cp.center, 
                            offset_color=oc)
        
        x_min, x_max, y_min, y_max = update_xy_limits(x_min, 
                            x_max, 
                            y_min, 
                            y_max, 
                            xi, 
                            xj, 
                            yi, 
                            yj)

    return x_min-gp.fp.offset_boundaries, x_max+gp.fp.offset_boundaries, \
        y_min-gp.fp.offset_boundaries, y_max+gp.fp.offset_boundaries

def adapt_lims(ax, gp: GlyphsParameters):
    if gp.fp.set_lims:
        for i in range(gp.fp.nx):
            x_lims = ax[i, gp.fp.ny-gp.fp.offset_j-1].get_xlim()
            y_lims = ax[i, gp.fp.ny-gp.fp.offset_j-1].get_ylim()
            for j in range(gp.fp.ny-gp.fp.offset_j):
                ax[i, j].set_xlim(x_lims)
                ax[i, j].set_ylim(y_lims)


def glyphs(gp: GlyphsParameters):
    
    """ This function generates a grid of glyphs. 
    The glyphs are generated by computing the minimum spanning tree of a graph and then plotting
    the edges of the tree. The glyphs are generated for a range of values of N in the vertical axis, 
    and an increasing number of edges in the horizontal axis. 
    

    """
    final_fig, final_ax = create_figure(gp.fp)
    set_background_color(final_fig, gp.cp)

    for i in range(0,gp.fp.nx):

        n = gp.fp.offset_n+i
        params = get_parameters(n, gp.pp)
        change_color(params, gp.cp)
        set_prefix(params, gp.cp)

        graph, _ = tiling.compute(params)
        xs, ys = get_xs_ys(graph)

        edges_accepted = acm_kruskal.compute(graph, [0,0])

        for j in range(gp.fp.offset_j,gp.fp.ny):
            
            this_j = j-gp.fp.offset_j
            ax = final_ax[i,this_j]
            ax.axis('off')
          
            number_of_edges = int((j+1)*gp.fp.offset_edge**2)
            edges_accepted_local = edges_accepted[:number_of_edges]

            offset_color_local = gp.cp.offset_color(i,j)

            x_min_b, x_max_b, y_min_b, y_max_b = plot_one_glyph(ax, edges_accepted_local, xs, ys, gp, params, offset_color_local)
             
            ax.set_xlim(x_min_b, x_max_b)
            ax.set_ylim(y_min_b, y_max_b)
        
        
    adapt_lims(final_ax, gp)
    final_fig.set_size_inches(gp.fp.ny-gp.fp.offset_j, gp.fp.nx)
    plt.show()
    fig_name = f'glyphs_{gp.hash_name()}.png'
    final_fig.savefig(fig_name, dpi=300)


if __name__ == "__main__":

    gp = GlyphsParameters(GlyphsColorsParameters(offset_color=default_offset_color,
                                                 white_bg=False,
                                                 colored_edges=True),
                          GlyphsFigureParameters(ny=4, 
                                                 nx=4, 
                                                 offset_edge=2, 
                                                 offset_boundaries=0.7, 
                                                 offset_j=0, 
                                                 offset_n=3, 
                                                 set_lims=True),
                          GlyphsParametersParameters(functionToMapN=default_functionToMapN,))
    glyphs(gp)



    gp.cp =  GlyphsColorsParameters(offset_color=alternative_offset_color, 
                                    white_bg=False,
                                    colored_edges=True,
                                    center = (3,1))
    glyphs(gp)