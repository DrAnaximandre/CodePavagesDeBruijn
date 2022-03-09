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
            #  nuance of blue
            h = np.random.uniform(170, 190)
            if s > 0:
                sat = 60 + np.cos((r * 20 + kr * 10 - ks * 5+s) * 2) * 40

            v = 50 + np.cos((s * 20 + kr * 20)) * 50
            v = 0 if v < 10 else v
            return rgb((h, sat, v))

        elif params.COLORING == 11:
            """ Joli rond coloré"""
            h = 200 * d / params.DMAX + 20
            h += 10*np.cos((s * 20 + kr*10 + ks*15-d)) + np.sin(2*(s * 20 + kr*10 + ks*15-d)) * 10
            sat = 50
            if d > params.DMAX * 0.8:
                sat = 80
            if d < params.DMAX * 0.2:
                sat = 99

            v = 50 + np.cos((s * 20 + kr * 10 + ks * 15 - d)) * 20 + np.sin(2 * (s * 20 + kr * 10 + ks * 15 - d)) * 24
            if v < 30:
                v= 95
            return rgb((h, sat, v))

        elif params.COLORING == 12:

            h = 215
            sat = 30 + np.cos((-s * 20 + kr * 10 * ks * 15 - d)) * 14 + np.sin(2 * (s * 20 - kr * 10 + ks * 15 - d)) * 16
            v = 50 + np.cos((s * 20 + kr * 10 + ks * 15 - d)) * 24 + np.sin(2 * (s * 20 + kr * 10 + ks * 15 - d)) * 24

            return rgb((h, sat, v))

        elif params.COLORING == 13:
            """ Joli rond coloré partant du rouge au centre"""
            h = 500 * d / params.DMAX -100
            h += 12 * s - 3*ks
            h= h%360
            sat = 45
            sat += np.cos((s * 20 + kr * 10 + ks * 15 - d)) * 29 + np.sin(2 * (s * 20 + kr * 10 + ks * 15 - d)) * 24
            sat = sat%100
            if sat < 30:
                sat = 95

            v  = 50 + np.cos((s * 2 + kr * 15 + ks * 10 - d)) * 24 + np.sin(2 * (s * 20 + kr * 10 + ks * 15 - d)) * 24

            return rgb((h, sat, v))

        elif params.COLORING == 14:
            """ Rouge noir blanc gris"""

            r1 = (131, 2, 19)
            r2 = (154,0,2)
            r3 = (179, 13, 2)
            r4 = (240, 234, 228)
            r5 = (88, 88, 88)
            r6 = (26, 26, 26)
            L = np.array([r1,r2,r3,r4,r5,r6])
            k = int(np.cos(d)*np.pi)%6

            return L[k]/255
        elif params.COLORING == 15:
            """???"""

            h = (ks+s)%360
            s = (int(np.sin(d*5) * 125) +126)/2.6
            v = (int(np.cos(2*d) * 20 + np.sin(d*2)*15) + 255-35)/2.6

            return rgb((h,s,v))
        else:
            print("COLORING=" + str(params.COLORING) + " is not defined !")
            exit
