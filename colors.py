import math
import matplotlib.colors as clrs
import numpy as np

from parameters import Parameters, WHITE


#######################################

def mapR(x, xD, xF, yD, yF) :
    return yD + (yF-yD)/(xF-xD)*(x-xD)

def shape_rhombus(r, s, params):
    """ the shape_rhombus of a rhombus corresponds to its 'thickness'
        and ranges from 1 to floor(N/2) """
    i = s - r
    if i > params.N / 2:
        i = params.N - i
    return i

def rgb(my_hsv) :
    (h,s,v) = my_hsv
    c = (h/360, s/100, v/100)
    return clrs.hsv_to_rgb(c)

# HSB color mode : H : hue; S = saturation; B : brightness
# some specific colors (HSB color mode)
# note : HSB and HSV are the same
C1 = (198, 86, 40)  # dark blue
C2 = (180, 100, 64)  # cyan fonce
#C3 = (47, 9, 96)  # 'broken' white
C3 = (47, 9, 80)  # 'broken' light grey
C4 = (39, 85, 66)  # light brown
#C5 = (119, 39, 58)  # prussian green
C5 = (150, 39, 20)  # dark prussian green
C = list(map(rgb, [C3, C2, C4, C5, C1]))


######### the main function for coloring ##########

#NBF = math.floor(N / 2)  # number of different shapes


    #colors = ['red','green','blue','cyan']
    #plt.fill(xc,yc,colors[f])
    #plt.fill(xc,yc,'C'+str(f))

def kolor(r, s, kr, ks, d, params):

    
    NBF = math.floor(params.N / 2)  # number of different shapes


    # no color (white)
    if params.COLORING == 0:
        return WHITE

    else:

        f = shape_rhombus(r, s, params) - 1  # in [0 .. NBF - 1]

        # colors depending on rhombus shape
        if params.COLORING == 1:
            #h = f * 360 / NBF
            h = f * 90 / NBF
            return rgb((h, 80, 70))

        # colors depending only on the distance to the origin (center of
        # screen)
        elif params.COLORING == 3:
            h = mapR(d, 0, params.DMAX, 120, 220)
            return rgb((h, 80, 70))

        # color depending on shape_rhombus and distance
        elif params.COLORING == 4:
            h = mapR(f, 0, NBF - 1, 110, 225)
            s = 100 - mapR(d, 0, params.DMAX, 0, 20)
            b = 100 - mapR(d, 0, params.DMAX, 0, 70)
            return rgb((h, s, b))

        # specific colors
        elif params.COLORING == 9:
            c = C[f % len(C)]
            return c
        elif params.COLORING == 10:
            h = np.random.uniform(170,190)

            if s > 0:
                sat = 40 + np.cos((r * 20 + kr * 30 - ks * 5) * 2) * 30

            v = 50 + np.cos((s * 20 + kr * 20)) * 50
            v = 0 if v < 10 else v
            return rgb((h, sat, v))

        elif params.COLORING == 11:
            """ Joli rond coloré"""
            h = 300 * d / params.DMAX
            # += 10*np.cos((s * 20 + kr*10 + ks*15-d)) + np.sin(2*(s * 20 + kr*10 + ks*15-d)) * 10
            sat = 50
            if d > params.DMAX * 0.8:
                sat = 80
            if d < params.DMAX * 0.2:
                sat = 100

            v = 50 + np.cos((s * 20 + kr * 10 + ks * 15 - d)) * 25 + np.sin(2 * (s * 20 + kr * 10 + ks * 15 - d)) * 25
            return rgb((h, sat, v))


        else:
            print("COLORING=" + str(params.COLORING) + " is not defined !")
            exit
