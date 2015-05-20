"""
A script to generate some custom lightcurves for the NGC1333 paper using plot4.

"""

from __future__ import division

import os

import numpy as np
import matplotlib.pyplot as plt
import atpy

from plot4 import lc_and_phase_and_colors, multi_lc_phase_colors, multi_lc_colors, basic_lc, StarData
from plot_perseus import NGC1333StarData


dropbox_figure_output = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/")
dropbox_bo_data = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/DATA/")
photometry_data = atpy.Table('{0}low_maxvars_photometry_aboveStetson0.5_fdece_gc0.95_s0.1_d0.5.fits'.format(dropbox_bo_data))


# f89 = p329
# ^ (from spreadsheet at: https://docs.google.com/spreadsheets/d/1RJmPr98S8LZ0rSrGGHgfW5E2hnnCW31E2Pe-IC8GXrg/edit#gid=1769727844)
# pid_array = np.array(preliminary_ID_column)
# maxvars.SOURCEID[ pid_array == 'p329']
f89_id = 44508746118971

# f95 = p337
# maxvars.SOURCEID[ pid_array == 'p337']
f95_id = 44508746116800


def eightpanel_f95(**kwargs):
    period = 26.42
    stardata = NGC1333StarData(photometry_data, f95_id)

    fig = lc_and_phase_and_colors(stardata, period, offset=0.32, **kwargs)

    fig.ax_k_lc.set_xlim(0,250)
    fig.ax_jhk.set_xlim(-0.3,2.2)
    fig.ax_jhk.set_ylim(-0.3,2.2)

    return fig

def save_f95():
    eightpanel_f95().savefig(dropbox_figure_output+"f95_lc.pdf", bbox_inches='tight')




