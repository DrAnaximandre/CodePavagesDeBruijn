###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################
import matplotlib
matplotlib.use('Qt5Agg')
from go import *
import json
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description='Process configuration file.')

# Add the argument for the config file
parser.add_argument('-c', '--config', type=str, default='configs/config_polo.json',
                    help='Path to the configuration file')

# Add the argument for the go function
parser.add_argument('-g', '--go', type=str, default='goAllDefaults',
                    help='Name of the go function to run')

# Parse the command line arguments
args = parser.parse_args()

# Load the configuration file
with open(args.config, 'r') as config_file:
    config = json.load(config_file)

# Map function names to actual functions
go_functions = {
    'goAllDefaults': goAllDefaults,
    'goVerySmall': goVerySmall,
    'goLivret': goLivret,
    'goLivretVar': goLivretVar,
    'goCentralSymetry': goCentralSymetry,
    'goNotExactSymetry': goNotExactSymetry,
    'goDeBruijnRegular': goDeBruijnRegular,
    'goPentaville': goPentaville,
    'goPentavilleS': goPentavilleS
}

# Get the go function 
try:
    go_function = go_functions[args.go]
except KeyError:
    print(f"Function {args.go} not found.")

# Run the go function
go_function(config)

###########  Polo's

# goDemo()
# goPolo(N=5)
# goPoloCubes(17)
#
# P = ParallelProcessor()
# P.add(goPoloCubes)
# P.run(np.arange(14, 19, 0.5))

########## Mike's


#goPentavilleS()
# goPentavilleVariation()
