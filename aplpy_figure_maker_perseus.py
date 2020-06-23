"""

This is a script for making images & figures for NGC1333 that require APLpy.

Each figure (or, sometimes, group of closely related figures) is generated
by its own function, so that you don't HAVE to regenerate them all at the same
time if you only want one.

"""


import os

import numpy as np

import aplpy

big_image_path = os.path.expanduser("~/Downloads/")

def m42_map(xmarker_array=None, ymarker_array=None, rect=True, latex=True):
    """
    Shows our field on top of VISTA's great M42 image.

    Parameters
    ----------
    xmarker_array, ymarker_array : numpy.ndarrays
        X and Y coordinates (here, R.A. and Decl.) of the markers to plot
    rect : bool, optional
        Plot the rectangle demarcating our field?
    latex : bool, optional
        Use LaTeX to render the text and labels?

    Returns
    -------
    fig : aplpy.FITSFigure

    """

    fig = aplpy.FITSFigure(big_image_path+"NGC1333_ha.fits", north=True)

    fig.show_rgb(big_image_path+"eso1006a.jpg")

    center_of_box_ra = np.degrees(maxvars.RA.min() +
                                  maxvars.RA.max())/2
    center_of_box_dec= np.degrees(maxvars.DEC.min() +
                                  maxvars.DEC.max())/2

    width_of_box_ra = np.degrees(maxvars.RA.max() -
                                 maxvars.RA.min())
    width_of_box_dec = np.degrees(maxvars.DEC.max() -
                                  maxvars.DEC.min())

    fig.show_rectangles(center_of_box_ra, center_of_box_dec,
                        width_of_box_ra, width_of_box_dec,
                        color='y', lw=3)

    if xmarker_array != None and ymarker_array != None:
        fig.show_markers(xmarker_array, ymarker_array,
                         marker='+',edgecolor='w', s=40)

        fig.show_markers(xmarker_array, ymarker_array,
                         marker='o',edgecolor='r', s=2)

    northeast_corner = (np.degrees(maxvars.RA.max() + 0.001),
                        np.degrees(maxvars.DEC.max() + 0.001))

    southwest_corner = (np.degrees(maxvars.RA.min() - 0.001),
                        np.degrees(maxvars.DEC.min() - 0.001))

    px_northeast_corner = fig.world2pixel(northeast_corner[0], northeast_corner[1])
    px_southwest_corner = fig.world2pixel(southwest_corner[0], southwest_corner[1])
    
    plt.xlim(px_northeast_corner[0], px_southwest_corner[0])

    plt.ylim(px_southwest_corner[1], px_northeast_corner[1])

    if latex:
        fig.set_system_latex(True)

    return fig
 
