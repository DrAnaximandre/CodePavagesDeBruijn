import math
import matplotlib.colors as clrs
from matplotlib import path
import numpy as np

from parameters import Parameters, WHITE
from itertools import combinations

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

def kolor(r, s, kr, ks, d, params, x, y):

    NBF = math.floor(params.N / 2)  # number of different shapes

    # no color (white)
    if params.COLORING == 0:
        return (0,0,0)

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
            h = mapR(f, -1, NBF - 1, 110, 225)
            s = 100 - mapR(d, 0, params.DMAX, 0, 20)
            b = 100 - mapR(d, 0, params.DMAX, 0, 70)
            return rgb((h, s, b))

        # specific colors
        elif params.COLORING == 9:
            c = C[f % len(C)]
            return c

        elif params.COLORING == 10:
            #  nuance of blue
            # h = 180  + 10 * np.arctan(x[0]+y[0])
            # if s > 0:
            #     sat = 60 + np.cos((r * 20 + kr * 10 - ks * 5+s) * 2) * 4
            # v = 50 + np.cos((s * 20 + kr * 20)) * 50
            # v = 0 if v < 10 else v

            h = 200
            sat = 50
            v = 70


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

            n_colors = 6
            ldc = list(combinations(range(n_colors),2))
            comb = len(ldc)

            L = np.zeros((comb,3))

            L[0,: ] = (131,2,19)
            L[1,: ] = (25, 25, 25)
            L[2,: ] = (200,23,210)
            L[3, :] = (179, 13, 2)
            L[4, :] = (250, 250, 250)
            L[5, :] = (99, 99, 99)

            # we do the average between each combination of colors
            for i in range(comb):
                L[i, :] = (L[ldc[i][0], :] + L[ldc[i][1], :]) / 2

            i1 = int(np.mean(x[0]+y[1]+ 0.22*x[2]+y[2]))%comb
            i2 = int(np.mean(x[1]-y[2]))%comb
            ctr = np.mean(L[[i1, i2]], axis=0)
            return ctr/255


        elif params.COLORING == 15:
            """???"""

            dp = 1-np.mean(x*y)/2

            h = (ks+s+r+200-kr)%360
            s = (int(np.sin(dp*5) * 125) + 126)/2.6
            v = (int(np.cos(2*d+s/(1.2+ks)) * 20 + np.sin(d*2+kr)*15) + 255-35)/2.6

            return rgb((h,s,v))

        elif params.COLORING == 16:
            """photo simple"""
            xm = (np.mean(x)/params.DMAX+params.DMAX)/2
            ym = (np.mean(y)/params.DMAX+params.DMAX)/2
            ims = params.image.shape
            xm_c = int(xm * ims[0])
            ym_c = int(ym * ims[1])

            col_at_pix = params.image[xm_c, ym_c]
            return col_at_pix/255


        elif params.COLORING == 17:
            """photo plus compliqué mais pas trop"""
            ims = params.image.shape

            xm_c = [int((xe + params.DMAX) / (params.DMAX * 2) * ims[0]) for xe in x]
            ym_c = [int((ye + params.DMAX) / (params.DMAX * 2) * ims[1]) for ye in y]

            mx = min(xm_c), max(xm_c)
            my = min(ym_c), max(ym_c)

            image_bloc = params.image[mx[0]:(mx[1]+1), my[0]:(my[1]+1)]
            if image_bloc.shape[0] != 0  and image_bloc.shape[1] !=0:
                col_at_pix = image_bloc.mean(0).mean(0)/255
            else:
                col_at_pix = (0, 0, 0)
            return col_at_pix


        elif params.COLORING == 18:
            """photo plus compliqué, ne marche pas encore"""
            ims = params.image.shape

            xm_c = [int((xe + params.DMAX) / (params.DMAX * 2) * ims[0]) for xe in x]
            ym_c = [int((ye + params.DMAX) / (params.DMAX * 2) * ims[1]) for ye in y]

            mx = min(xm_c), max(xm_c)
            my = min(ym_c), max(ym_c)

            image_bloc = params.image[mx[0]:mx[1], my[0]:my[1]]

            xv, yv = np.meshgrid(np.arange(image_bloc.shape[0]), np.arange(image_bloc.shape[1]))
            p = path.Path([ bob for bob in zip(xm_c, ym_c)])
            flags = p.contains_points(np.hstack((xv.flatten()[:, np.newaxis], yv.flatten()[:, np.newaxis])))
            print(flags.shape)
            col_at_pix = image_bloc.mean(0).mean(0)/255
            return col_at_pix

        elif params.COLORING == 19:
            """???"""

            dp = 1-np.mean(x)/2

            h = (dp+125)%360
            s = (int(np.sin(d*2) * 50) + 55)/2.1
            if s < 25:
                s=100

            v = (int(np.cos(3*dp) * 20 + np.sin(d*4)*15) + 125-35)/2.1
            if np.random.rand() < 0.1:
                v = 100
            return rgb((h,s,v))

        elif params.COLORING == 23:

            gradations = np.arange(-20, 20, step=1)

            n_grads = gradations.shape[0]
            red = 0
            blue = 0
            green = 0

            for j, une_gradation in enumerate(gradations):

                c1r = np.sqrt(d*2) < j/n_grads
                c2r = np.mean(x)/np.mean(y) < 1

                if c1r and c2r:
                    red += (1 - np.sin(2*np.pi*j/n_grads)/10)/n_grads
                else:
                    red += 0.4 + 0.2*np.sin(2*np.pi*j/n_grads)/10

                if r*s/(1+np.sin(ks)) >= 0.1:
                    blue += (1-np.sin(une_gradation))/(3)
                if kr*ks >= f:
                    green += np.cos(0.5*j/n_grads)/n_grads
                elif c1r:
                    green += 0.4/n_grads
                else:
                    green += j/n_grads + np.sin(kr/(r+0.001))/n_grads

            # print(red,green, blue)
            return ((red/n_grads,green/n_grads,blue/n_grads))


        else:
            print("COLORING=" + str(params.COLORING) + " is not defined !")
            exit
