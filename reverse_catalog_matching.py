"""
This is a script where we use literature catalogs as a PRIMARY table

and match our own data to that, rather than vice-versa.
It's a good way of quantifying the variability of previously-known young stars.

"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from tablemate_core import TableParameters, tablemater
from perseus_star_counter import q2_stars, q1_stars
from tablemate_script_perseus import Gutermuth_2008, Getman_2002

q2_wfcam_stars = TableParameters(
    data = q2_stars,
    alias = "WFCAM_q2_stars",
    full_name = "Master spreadsheet for 2147 stars in the UKIRT data that have 'pristine' data quality in all 3 bands.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID',
    max_match=2.0)

q1_wfcam_stars = TableParameters(
    data = q1_stars,
    alias = "WFCAM_q1_stars",
    full_name = "Master spreadsheet for 979 stars in the UKIRT data that have 'pristine' data quality in only 1 or 2 bands.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID')


def match_spitzer_to_ukirt():
    """ 
    A function that performs an "inverse" cross-match between 
    mid-IR selected sources from Spitzer/Gutermuth2008, and our UKIRT stars.

    """

    # Produces a table of cross-match IDs and indices.
    mated_spitzer = tablemater(Gutermuth_2008, q2_wfcam_stars)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # in approximate english: "the stats table, where you take the row 
    # handed to you by the mated table, but only where there's a match"
    # Q2
    ax.hist( 
        q2_stars.Stetson[ 
            mated_spitzer.where(mated_spitzer['WFCAM_q2_stars_index'] != -1)['WFCAM_q2_stars_index'] 
            ], 
        range=[0,20], bins=60, color='b', label="Q=2"
        )

    ax.set_xlabel("Stetson Index")
    ax.set_ylabel("Number of stars which are in both UKIRT(Q=2) and SpYSO")
    ax.set_title("Variability of YSOs from Gutermuth et al. 2008")

    fig_range = plt.figure()
    ax_range = fig_range.add_subplot(1,1,1)

    # in approximate english: "the stats table, where you take the row 
    # handed to you by the mated table, but only where there's a match"
    # Q2
    ax_range.hist( 
        q2_stars.k_ranger[ 
            mated_spitzer.where(mated_spitzer['WFCAM_q2_stars_index'] != -1)['WFCAM_q2_stars_index'] 
            ], 
        range=[0,2], bins=20, color='b', label="Q=2"
        )

    ax_range.set_xlabel(r"$\Delta K$ (mag)")
    ax_range.set_ylabel("Number of stars which are in both UKIRT(Q=2) and SpYSO")
    ax_range.set_title("Variability of YSOs from Gutermuth et al. 2008")

    return mated_spitzer


def match_chandra_to_ukirt():
    """ 
    A function that performs an "inverse" cross-match between 
    X-ray selected sources from Chandra/Getman2002, and our UKIRT stars.

    """

    # Produces a table of cross-match IDs and indices.
    mated_chandra = tablemater(Getman_2002, q2_wfcam_stars)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # in approximate english: "the stats table, where you take the row 
    # handed to you by the mated table, but only where there's a match"
    # Q2
    ax.hist( 
        q2_stars.Stetson[ 
            mated_chandra.where(mated_chandra['WFCAM_q2_stars_index'] != -1)['WFCAM_q2_stars_index'] 
            ], 
        range=[0,20], bins=60, color='b', label="Q=2"
        )

    ax.set_xlabel("Stetson Index")
    ax.set_ylabel("Number of stars which are in both UKIRT(Q=2) and Chandra/ACIS")
    ax.set_title("Variability of X-ray sources from Getman et al. 2002")

    fig_range = plt.figure()
    ax_range = fig_range.add_subplot(1,1,1)

    # in approximate english: "the stats table, where you take the row 
    # handed to you by the mated table, but only where there's a match"
    # Q2
    ax_range.hist( 
        q2_stars.k_ranger[ 
            mated_chandra.where(mated_chandra['WFCAM_q2_stars_index'] != -1)['WFCAM_q2_stars_index'] 
            ], 
        range=[0,2], bins=20, color='b', label="Q=2"
        )

    ax_range.set_xlabel(r"$\Delta K$ (mag)")
    ax_range.set_ylabel("Number of stars which are in both UKIRT(Q=2) and Chandra/ACIS")
    ax_range.set_title("Variability of YSOs from Getman et al. 2002")

    return mated_chandra
