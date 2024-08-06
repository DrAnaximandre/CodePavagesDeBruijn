###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from go import *
from utils import ParallelProcessor
import json

# Load the configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Accessing the configuration
config = config.get('Polo')

###########  Polo's

#goDemo()
#goPolo(5, config_file=config)
# goPoloCubes(17)
#
# P = ParallelProcessor()
# P.add(goPoloCubes)
# P.run(np.arange(14, 19, 0.5))

########## Mike's
#
goAllDefaults(config=config)# uses all config defaults
# goVerySmall()
#
# goLivret() # does not display but saves pdf
# goLivretVar() # does not display but saves pdf, and does not quit
#
# goCentralSymetry()
# goNotExactSymetry()
# goDeBruijnRegular(6)
# goPentaville()
# goPentavilleS()
# goPentavilleVariation()
