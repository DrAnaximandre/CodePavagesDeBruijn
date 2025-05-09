###########################################################################
#  Comments and suggestions are welcome. Mail to :  mike.lembitre@gmail.com
###########################################################################
import matplotlib
matplotlib.use('Qt5Agg')
from go import *
from config_reader import get_config
from go_glyphs import go_glyphs

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
    'goPentavilleS': goPentavilleS,
    'goPentavilleVariation': goPentavilleVariation,
    'goPolo': goPolo,
    'goPoloCubes': goPoloCubes,
    'goDemo': goDemo,
    'goGlyphs': go_glyphs,
}

if __name__ == "__main__":

    # Get the configuration and arguments
    config, args = get_config()

    # Get the go function 
    try:
        go_function = go_functions[args.go]
    except KeyError:
        print(f"Function {args.go} not found.")

    # Run the go function
    go_function(config)
