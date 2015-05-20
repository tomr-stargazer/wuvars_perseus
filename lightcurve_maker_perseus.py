"""
A script to generate some custom lightcurves for the NGC1333 paper using plot4.

"""

from __future__ import division

import os

import numpy as np
import matplotlib.pyplot as plt
import atpy

from plot4 import lc_and_phase_and_colors, multi_lc_phase_colors, multi_lc_colors, basic_lc, StarData, lightcurve_axes_with_info, phase_axes_with_info, colormag_axes
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



def custom_fivepanel_f89():
    period = 14.4
    stardata = NGC1333StarData(photometry_data, f89_id)

    stardata.s_table['KPPERRBITS'] *= 0
    stardata.s_table['HPPERRBITS'] *= 0

    fig = custom_HK_fivepanel(stardata, period, offset=-0.3)
    fig.ax_k_lc.set_xlim(0,250)

    fig.ax_k_phase.set_xlim(-0.1, 1.1)

    return fig

def save_f89():
    custom_fivepanel_f89().savefig(dropbox_figure_output+"f89_lc.pdf", bbox_inches='tight')


def custom_HK_fivepanel(stardata, period=None, custom_xlabel=False, time_cmap='jet', offset=0):
    """
    Generates a custom eight-panel lightcurve: phase-folded, straight, and color info.

    """

    # kwargs defaulting over
    # time_cmap = 'jet'
    color_slope = False

    colorscale='date'

    stretch_factor = 1.575

    fig = plt.figure(figsize = (10*stretch_factor, 6), dpi=80, facecolor='w', edgecolor='k')

    bottom = 0.1
    height = .25
    left = 0.075 / stretch_factor
    width = 0.5 / stretch_factor

    ax_k_lc = fig.add_axes( (left+(left+width)-0.2, bottom, width, height) )
    ax_h_lc = fig.add_axes( (left+(left+width)-0.2, bottom+.3, width, height), sharex=ax_k_lc )

    ax_k_phase = fig.add_axes( (left+0.015, bottom, width/3, height) )
    ax_h_phase = fig.add_axes( (left+0.015, bottom+.3, width/3, height), sharex=ax_k_phase )

    color_height = 0.375
    color_left = 0.65 / stretch_factor + (left+width)
    color_width = 0.3 / stretch_factor

    ax_khk = fig.add_axes( (color_left-0.2, bottom, color_width+0.07, height+0.3) )

    d_ax_lc = {'h': ax_h_lc, 'k': ax_k_lc}
    d_ax_phase = {'h': ax_h_phase, 'k': ax_k_phase}

    d_cmap=time_cmap

    if type(d_cmap) is str:
        d_cmap = {'j': d_cmap, 'h': d_cmap, 'k': d_cmap}
    elif type(d_cmap) is not dict:
        d_cmap = {'j': d_cmap[0], 'h': d_cmap[1], 'k': d_cmap[2]}

    color_vmin = stardata.min_date
    color_vmax = stardata.max_date 

    vmin = color_vmin
    vmax = color_vmax

    for band in ['h', 'k']:
        lightcurve_axes_with_info(stardata, band, d_ax_lc[band], colorscale,
                                  cmap=d_cmap[band], vmin=vmin, vmax=vmax)

        phase_axes_with_info(stardata, band, period, d_ax_phase[band], colorscale,
                                  cmap=d_cmap[band], vmin=vmin, vmax=vmax, offset=offset)

    colormag_axes(stardata, 'khk', ax_khk, colorscale, cmap=time_cmap, vmin=vmin, vmax=vmax,
                  color_slope=color_slope)

    # Hide the bad labels...
    plt.setp(ax_h_lc.get_xticklabels(), visible=False)
    plt.setp(ax_h_phase.get_xticklabels(), visible=False)

    # Label stuff
    if custom_xlabel:
        ax_k_lc.set_xlabel( custom_xlabel )
    else:
        ax_k_lc.set_xlabel( "Time (MJD - %.1f)" % stardata.date_offset )

    ax_k_phase.set_xlabel("Phase (Period = {0:.4} days)".format(period))        

    ax_h_phase.set_ylabel( "H",{'rotation':'horizontal', 'fontsize':'large'} )
    ax_k_phase.set_ylabel( "K",{'rotation':'horizontal', 'fontsize':'large'} )

    ax_h_lc.set_ylabel( "H",{'rotation':'horizontal', 'fontsize':'large'} )
    ax_k_lc.set_ylabel( "K",{'rotation':'horizontal', 'fontsize':'large'} )

    ax_khk.set_xlabel( "H-K" )
    ax_khk.set_ylabel( "K", {'rotation':'horizontal'})

    fig.ax_k_lc = ax_k_lc
    fig.ax_h_lc = ax_h_lc

    fig.ax_k_phase = ax_k_phase
    fig.ax_h_phase = ax_h_phase

    fig.ax_khk = ax_khk

    return fig