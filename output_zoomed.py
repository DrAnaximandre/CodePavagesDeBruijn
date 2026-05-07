import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import numpy as np
from pathlib import Path

from parameters import Parameters
import io
from colors import kolor

from PIL import Image
Image.MAX_IMAGE_PIXELS = 19000**3

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def _crop_img(img, x1, x2, y1, y2, margin=0.1):
    """Crop image array to the given normalized coordinates with a margin."""
    h, w = img.shape[:2]
    x1m = max(0, x1 - margin)
    x2m = min(1, x2 + margin)
    y1m = max(0, y1 - margin)
    y2m = min(1, y2 + margin)
    c1 = int(x1m * w)
    c2 = int(x2m * w)
    r1 = int(y1m * h)
    r2 = int(y2m * h)
    return img[r1:r2, c1:c2], (x1m, x2m, y1m, y2m)


def _add_inset(ax, img, col, w, x1, x2, y1, y2, inset_bounds,
               connector_styles=None,  indicator_lw=None):
    """Add a zoomed inset to ax showing the region (x1,x2,y1,y2) of img.

    connector_styles: dict {index: (style_string_or_None, linewidth)}
    """
    axins = ax.inset_axes(inset_bounds, xlim=(x1, x2), ylim=(y1, y2),
                          xticklabels=[], yticklabels=[])
    axins.set_xticks([])
    axins.set_yticks([])

    cropped, ext = _crop_img(img, x1, x2, y1, y2)
    axins.imshow(cropped, extent=ext, origin="lower", aspect="auto")
    del cropped

    for spine in axins.spines.values():
        spine.set_color(col)
        spine.set_linewidth(w)

    iz = ax.indicate_inset_zoom(axins, edgecolor=col, alpha=1, linewidth=w)
    iz.rectangle.set_linewidth(indicator_lw if indicator_lw is not None else w)

    if connector_styles:
        for idx, (style, lw) in connector_styles.items():
            if style:
                iz.connectors[idx].set_connectionstyle(style)
            iz.connectors[idx].set_linewidth(lw)

    return axins, iz


def output_zoomed(fn, params):


    print(f"opening {fn}")
    img = np.asarray(Image.open(fn))
    print(img.shape)

    fig, ax = plt.subplots(figsize=(12,12))
    
    plt.axis('off')
    plt.title(params.title(), fontsize=7, y=0, pad=-30.)



    xmin, xmax, ymin, ymax = 0.2, 0.8, 0.2, 0.8
    cropped_main, ext_main = _crop_img(img, xmin, xmax, ymin, ymax)
    ax.imshow(cropped_main, extent=ext_main, origin="lower", aspect="auto")
    del cropped_main
    lim = params.DMAX* params.c
    left, bottom, width, height = 0.2, 0.2, 0.6,0.6
    p = plt.Rectangle((left, bottom), width, height, fill=False, linewidth=7.5)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.add_patch(p)

    col = "black"
    w = 2

    _add_inset(ax, img, col, w,
                0.48, 0.5, 0.5, 0.52,
                [0.05, 1 - 0.05 - 0.3125, 0.3125, 0.3125],
                connector_styles={0: ("Arc3, rad=-0.3", w ),
                                    3: ("Arc3, rad=0.3",  w )},
                )

    _add_inset(ax, img, col, w,
                 0.36, 0.37, 0.45, 0.46,
                [0.05, 0.1225, 0.2, 0.2],
                connector_styles={2: ("Arc3, rad=-0.3", w ),
                                    1: ("Arc3, rad=0.3",  w )},
                )

    w3, h3, x1_3, y1_3 = 0.005, 0.01, 0.5255, 0.61
    _add_inset(ax, img, col, w,
                x1_3, x1_3 + w3, y1_3, y1_3 + h3,
                [0.82, 0.7, 0.1, (h3 / w3) * 0.1],
                )
   
    
    w4, h4, x1_4, y1_4 = 0.03, 0.01, 0.5, 0.47
    _add_inset(ax, img, col, w,
                x1_4, x1_4 + w4, y1_4, y1_4 + h4,
                [0.5, 0.1, 0.3, (h4 / w4) * 0.3],
                )
    

    del img


    img_buf = io.BytesIO()
    fig.savefig(img_buf, format="tif", dpi=300) 
    img_buf.seek(0)
    pil_image = Image.open(img_buf)
    pil_image.convert('CMYK')
    pil_image.save(fn[:-4] + "_zoomed" + '.tif')
    
    fig.savefig(fn[:-4] + "_zoomed" + '.png', dpi=300)
    fig.show()



