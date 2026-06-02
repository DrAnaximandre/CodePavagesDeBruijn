import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy

import seaborn as sns

# TODO : montrer les palettes prédéfinies de seaborn
# TODO : dans les visualisations de palettes, il faut que les noms soient les notres
# TODO : faire un pdf des palettes disponibles


"""
   On trouvera ici une collection de palettes de couleurs (ou colormaps)
   utilisables comme des cmaps de matplotlib
   
   Une couleur est un quadruplet RGBA
   
   L'idée est d'avoir, pour cette application, une manière uniforme
   d'utiliser les colormaps/palettes, quelles que soient les manières
   de les dfinir
   
   ATTENTION 
   
       L'usage prévu des cmaps/palettes dans notre application est la suivante :
       Une cmap/palette est une fonction qui prend un float dans [0 ; 1] 
       (appelé 'index' dans la fonction exemples ci-dessous)
       et rend une couleur (possiblement une interpolation entre les couleurs
       de la palette)
       
       Si l'index est un entier le résultat dépend de la cmap/palette
       C'est déconseillé
         
        Voir exemples ci-dessous
  
"""


# un dictionnaire de colormaps / palettes
DIC_PALETTES = {}

def add(nom, cmap) : DIC_PALETTES[nom] = cmap

def get(nom) : return DIC_PALETTES[nom]



############################################  nos matplotlib colormaps ##################

add('TWILIGHT', plt.get_cmap('twilight'))

add('HSV', plt.get_cmap('hsv'))


############################################# nos seaborn palettes #####################

add('CUBELIX', sns.cubehelix_palette(as_cmap=True))
add('CUBELIX1', sns.cubehelix_palette(as_cmap=True, n_colors=4,
                                      start=2.5, rot=-2, dark=.8, light=.4, gamma=1.5, hue=1))
add('CUBELIX2', sns.cubehelix_palette(as_cmap=True, start=.2, rot=.65,  dark=.3, light=.7, ))

add('HLS', sns.color_palette('hls', as_cmap=True))
add('HUSL', sns.husl_palette(as_cmap=True))

#######################################################

NOMS_PALETTES = DIC_PALETTES.keys()
PALETTES = DIC_PALETTES.values()

#print('nos palettes : ' , NOMS_PALETTES)


###########################################################
#### nos palettes en RGBA               ##################
###########################################################

def str_color(color) :
    return '    color = ' + '  '.join([ f'{x:.4f}' for x in color ])

def nos_palettes_RGBA() :
    for (nom, cmap) in DIC_PALETTES.items() :
        print(f'{nom=}')
        for index in [0.0, 0.3, 0.5, 0.9, 1.0] :
            print(f'       {index=} ' +  str_color(cmap(index)))

# nos_palettes_RGBA()

############################################################################################
########## utilitaire pour visualiser nos palettes / colormaps (d'après la doc de matplotlib)
############################################################################################

gradient = numpy.linspace(0, 1, 256)
gradient = numpy.vstack((gradient, gradient))

def plot_color_gradients():
    # Create figure and adjust figure height to number of colormaps
    nrows = len(DIC_PALETTES)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)
    axs[0].set_title(f'nos colormaps/palettes', fontsize=14)

    for ax, nom in zip(axs, NOMS_PALETTES):
        ax.imshow(gradient, aspect='auto', cmap=DIC_PALETTES[nom])
        #name = cmap if type(cmap) is str else cmap.name
        ax.text(-0.01, 0.5, nom, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    plt.show()

# plot_color_gradients()


###########################################################
####   Les palettes prédéfinies de seaborn ################   # TODO a finir
###########################################################



###########################################################################
########  Pour info, les colormaps déjà définies de matplotlib  ###########
###########################################################################


def plot_color_gradients_matplotlib(category, cmap_list):
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)
    axs[0].set_title(f'{category} colormaps', fontsize=14)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=mpl.colormaps[name])
        ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    plt.show()


def plot_colors_matplotlib() :
    plot_color_gradients_matplotlib('Perceptually Uniform Sequential',
                                    ['viridis', 'plasma', 'inferno', 'magma', 'cividis'])

    plot_color_gradients_matplotlib('Sequential',
                                    ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                          'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                          'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'])

    plot_color_gradients_matplotlib('Sequential (2)',
                                    ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                          'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                          'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'])

    plot_color_gradients_matplotlib('Diverging',
                                    ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                          'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
                          'berlin', 'managua', 'vanimo'])

    plot_color_gradients_matplotlib('Cyclic', ['twilight', 'twilight_shifted', 'hsv'])

    plot_color_gradients_matplotlib('Qualitative',
                                    ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                          'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                          'tab20c'])

    plot_color_gradients_matplotlib('Miscellaneous',
                                    ['flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                          'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                          'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                          'turbo', 'nipy_spectral', 'gist_ncar'])

#plot_colors_matplotlib()


