import os
import matplotlib.pyplot as plt
import io
import numpy as np
import tqdm
from datetime import date

from parameters import Parameters
from tiling import outputTiling
import gamma as gm

def create_folder_with_increment(folder):
    # Create a video folder in the specified folder
    index = 0
    fdv_base = os.path.join(folder, 'video')

    while True:
        fdv = f"{fdv_base}{index}/"
        try:
            os.mkdir(fdv)
            return fdv, index
        except FileExistsError:
            index += 1
def read_lines(filename):
    print('reading', filename)
    with open(filename, 'r') as f:
        lines = f.readlines()
        x1 = [float(line.split()[0]) for line in lines]
        y1 = [float(line.split()[1]) for line in lines]
        x2 = [float(line.split()[2]) for line in lines]
        y2 = [float(line.split()[3]) for line in lines]
        print('read', len(x1), 'points')

    MAX = len(x1)

    return MAX, x1, y1, x2, y2

def get_list_of_indices_at_which_plot_image(MAX,
                                            duration=10,
                                            fps=30,
                                            kind="old"):

    if kind == "old":
        # this  kinda works but not too well
        first_half = [int(i * (i + 1) // 2) for i in range(int(MAX ** 0.5))]
        result = first_half + [MAX - i for i in reversed(first_half)]

    if kind == "v1":
        # linear interpolation
        result = [int(i * MAX / duration / fps) for i in range(duration * fps)]
        result.append(MAX-1)

    # remove duplicates
    result = list(dict.fromkeys(result))

    return result

def decay_red(i):
    return 0.6 + 0.2 * np.sin(2 * np.pi * i/10/30 )

def video_from_lines(
        filename,
        folder='./results/22-aout/',
        dmax=10,
        dpi=300,
        size=1000,
        initial_color = [1,0.005,1,1],
        duration =10):

    fdv, index = create_folder_with_increment(folder)
    MAX, x1, y1, x2, y2 = read_lines(filename)


    # sort by proximity to the center
    x1 = np.array(x1)
    y1 = np.array(y1)
    x2 = np.array(x2)
    y2 = np.array(y2)
    d = np.sqrt(x1**2 + y1**2)
    idx = np.argsort(d)

    # # flip x1 and y1
    # x1, y1 = -np.array(x1), -np.array(y1)
    # # flip x2 and y2
    # x2, y2 = -np.array(x2), -np.array(y2)

    # # get index of x1, low to high
    # idx = np.argsort(x1)

    x1 = x1[idx]
    y1 = y1[idx]
    x2 = x2[idx]
    y2 = y2[idx]

    result = get_list_of_indices_at_which_plot_image(MAX, duration = duration)

    minx = -dmax
    miny = -dmax
    maxx = dmax
    maxy = dmax

    print('plotting')
    fig = plt.figure(figsize=(size/dpi, size/dpi), dpi=dpi, frameon=True, facecolor='black')
    ax = fig.add_subplot(111)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plt.xlim(minx, maxx)
    plt.ylim(miny, maxy)
    plt.axis('off')

    accx = []
    accy = []

    dvtc = {i : np.array([]) for i in range(1, 11)}
    for i in tqdm.tqdm(range(MAX)):
        x = [x1[i], x2[i]]
        y = [y1[i], y2[i]]
        accx.append(x)
        accy.append(y)

        if i in result:

            # initial_color[0] = np.sqrt(x1[i]**2 + y1[i]**2) / (10+dmax)
            # initial_color[1] = 1 / 2 + 0.4495 * np.cos(x1[i]/2)
            # initial_color[2] = 1 / 2 + 0.4495 * np.cos(y1[i]/2)


            if i !=0:

                image_data = np.array(bytearray(buffer.read()), dtype=np.uint8)
                image = plt.imread(io.BytesIO(image_data))

                # # select all point where there is somewhat some red
                image_red_index = image[:, :, 0] > 0.96
                #
                pr = 0
                pg = 0
                pb = 0

                cr = 0.9568
                cg = 0.949
                cb = 1
                #
                image[image_red_index,:] += [pr,pg,pb,0]
                image *= [cr, cg, cb, 1]

                fig = plt.figure(figsize=(size / dpi, size / dpi), dpi=dpi, frameon=True)
                ax = fig.add_subplot(111)

                plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
                f1 = ax.imshow(image, extent=[minx, maxx, miny, maxy])

                plt.xlim(minx, maxx)
                plt.ylim(miny, maxy)
                plt.axis('off')

            for xloc, yloc in zip(accx, accy):
                ax.plot(xloc,
                        yloc,
                        'o-',
                        color=initial_color,
                        markersize=1,
                        linewidth=0.35,
                        solid_joinstyle='round',
                        solid_capstyle='round',
                        markeredgecolor='none'
                        )


            accx = []
            accy = []

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # we still need to save for the video.
            plt.savefig(f'{fdv}{i:05d}.png', bbox_inches='tight', pad_inches=0, dpi=dpi)
    #
    # # repeat last frame a few times with color fading
    for j in range(60):

        image_data = np.array(bytearray(buffer.read()), dtype=np.uint8)
        bob = plt.imread(io.BytesIO(image_data))

        # chang
        bob_not_black_index = (bob[:, :, 0] > 0.01)
        bob[bob_not_black_index] *= [0.935, 1, 1, 1]
        # clip
        bob[bob > 1] = 1

        fig = plt.figure(figsize=(size / dpi, size / dpi), dpi=dpi, frameon=True)
        ax = fig.add_subplot(111)

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        f1 = ax.imshow(bob, extent=[minx, maxx, miny, maxy])

        plt.xlim(minx, maxx)
        plt.ylim(miny, maxy)
        plt.axis('off')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.savefig(f'{fdv}{i+j+1:05d}.png', bbox_inches='tight', pad_inches=0,dpi=dpi)
        plt.close()

    print('creating video')
    os.system(f"ffmpeg -r 25 -pattern_type glob -i '{fdv}*'.png  -vcodec libx264 -pix_fmt yuv420p -y {fdv}video{index}.mp4")

if __name__ == '__main__':

    """ example on how to use this file 
    (quite CPU intensive, still experimental)
    
    - create a folder for storing the video
    - create a gamma object
    - create a parameter object from the gamma object
    - create the tiling
    - create the video from the tiling 
    
    One does not have to recreate the tiling each time, one just need the _lines.txt file from a previous tiling.
    
    """

    today = date.today()
    folder = f'./results/{today}/'

    gamma = gm.MappedGammaParameter(
        N=8,
        initialShift=12.345,
        functionToMap=lambda s, j: 1 + j / 9 * s if j % 2 != 0 else -1,
    )

    p = Parameters(GAMMA=gamma,
                   R=7,
                   N=gamma.N,
                   NBL=5,
                   DMAX=25,
                   COLORING=2,
                   BACKGROUND='k',
                   STROKECOLOR='w',
                   SCALE_LINEWIDTH=10,
                   RECTANGLE=True,
                   DIAGONAL=True,
                   SIDES=True,
                   SAVE=True,
                   SQUARE=True,
                   SAVE_FORMAT='png',
                   TITLE=False,
                   FRAME=True,
                   OUTPUT_COORDINATES=True,
                   TILINGDIR=folder)
    outputTiling(p)

    filename = p.filename_lines()

    video_from_lines(filename,
                    folder=folder,
                    dmax=25,
                    dpi=300,
                    size=1000,
                    initial_color=[1, 0, 0, 1],
                    duration=5)