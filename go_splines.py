import gamma as gm
from parameters import Parameters
from parametersSplines import ParametersSplines
import splines



def splines_Livret4D():
    n=9
    dmax = 15
    #gamma = gm.MGPcentralSymetry(n)
    gamma = gm.MGPnotExactSymetry(n)

    # parametres du pavage support
    # ParametersBook pour avoir les params de splines
    params = Parameters(
                            N=n, DMAX=dmax,
                            GAMMA=gamma,
                            SQUARE = False,
                            BACKGROUND='k',
                            SHOW=True,  save = True,
                            PARAMS_SPLINES=ParametersSplines()
    )

    params.PREFIX = 9999  # un truc bizarre nécessaire dans le code de Paul
    splines.splines(params)


splines_Livret4D()
