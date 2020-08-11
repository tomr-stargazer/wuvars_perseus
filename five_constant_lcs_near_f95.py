"""
Bo has asked for five "constant" light-curves near f95 so that we can demonstrate
that the dips in f95's light-curve is not due to data artifacts or anything.
(I'm not honestly worried about that being a problem, but we like to be thorough.)

"""

# we want just the J, H, K, time, and color columns.

import os
import numpy as np
import atpy
import astropy.table as tab

import matplotlib.pyplot as plt

from plot_perseus import NGC1333StarData

dropbox_bo_data = os.path.expanduser("~/Desktop/Bo_Tom/NGC1333/WSERV7/DATA/")
photometry_data = atpy.Table(
    "{0}low_maxvars_photometry_aboveStetson0.5_fdece_gc0.95_s0.1_d0.5.fits".format(
        dropbox_bo_data
    )
)
full_cleaned_data = atpy.Table(
    dropbox_bo_data + "fdece_graded_clipped0.95_scrubbed0.1_dusted0.5.fits"
)

f95_id = 44508746116800
f95_stardata = NGC1333StarData(photometry_data, f95_id)

path = os.path.expanduser("~/Desktop/Bo_Tom/NGC1333/WSERV7/")
constants = atpy.Table(path + "cleaning_products/constants_spreadsheet.fits")
ra, dec = f95_stardata.s_table["RA"].mean(), f95_stardata.s_table["DEC"].mean()

distance = ((constants["RA"] - ra) ** 2 + (constants["DEC"] - dec) ** 2) ** 0.5
constants.add_column("distance_from_f95", distance)
constants.sort("distance_from_f95")

for i, sid in enumerate(constants["SOURCEID"][:10]):

    ra_offset_arcsec = (
        np.degrees(constants[constants["SOURCEID"] == sid]["RA"][0] - ra) * 3600
    )
    dec_offset_arcsec = (
        np.degrees(constants[constants["SOURCEID"] == sid]["DEC"][0] - dec) * 3600
    )

    print(
        sid,
        f"\nRA offset: {ra_offset_arcsec:.1f}, DEC offset: {dec_offset_arcsec:.2f}\n",
    )

    this_fig = plt.figure(figsize=(16.42, 4.49))
    this_table = full_cleaned_data[full_cleaned_data["SOURCEID"] == sid]
    this_table["JAPERMAG3"][this_table["JAPERMAG3"] < 0] = np.nan
    this_table["HAPERMAG3"][this_table["HAPERMAG3"] < 0] = np.nan
    this_table["KAPERMAG3"][this_table["KAPERMAG3"] < 0] = np.nan

    plt.subplot(311)
    plt.errorbar(
        this_table["MEANMJDOBS"],
        this_table["JAPERMAG3"],
        fmt="b.",
        yerr=this_table["JAPERMAG3ERR"],
        ms=3,
    )
    plt.gca().invert_yaxis()
    plt.ylabel("J")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)
    plt.title(
        f"Constant #{i} near f95, {np.degrees(constants['distance_from_f95'][i])*60:.1f} arcmin away"
    )

    plt.subplot(312)
    plt.errorbar(
        this_table["MEANMJDOBS"],
        this_table["HAPERMAG3"],
        fmt="g.",
        yerr=this_table["HAPERMAG3ERR"],
        ms=3,
    )
    plt.gca().invert_yaxis()
    plt.ylabel("H")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.subplot(313)
    plt.errorbar(
        this_table["MEANMJDOBS"],
        this_table["KAPERMAG3"],
        fmt="r.",
        yerr=this_table["KAPERMAG3ERR"],
        ms=3,
    )
    plt.gca().invert_yaxis()
    plt.ylabel("K")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.xlabel("Modified Julian Date")
    plt.savefig(f"constant_{i}_near_f95.pdf")
    plt.savefig(f"constant_{i}_near_f95.png")
    # plt.savefig("fig_f95_for_Ben.png")


dropbox_bo_spread = dropbox_bo_data + "spreadsheet/"
spread = atpy.Table(
    dropbox_bo_spread + "fdece_graded_clipped0.95_scrubbed0.1_dusted0.5_spread.fits"
)
sp = spread

cand_case1 = (
    (sp.pstar_median > 0.75)
    & (
        (sp.N_j >= 50)
        & (sp.N_j <= 135)
        & (sp.j_mean > 11)  # J band criteria
        & (sp.j_mean < 17)
        & (sp.N_j_info == 0)
    )
    & (
        (sp.N_h >= 50)
        & (sp.N_h <= 130)
        & (sp.h_mean > 11)  # H band criteria
        & (sp.h_mean < 16.7)
        & (sp.N_h_info == 0)
    )
    & (
        (sp.N_k >= 50)
        & (sp.N_k <= 150)
        & (sp.k_mean > 11)  # K band criteria
        & (sp.k_mean < 16)
        & (sp.N_k_info == 0)
    )
)
q2_stars = sp.where(cand_case1)

distance_q2 = ((q2_stars["RA"] - ra) ** 2 + (q2_stars["DEC"] - dec) ** 2) ** 0.5
q2_stars.add_column("distance_from_f95", distance_q2)
q2_stars.sort("distance_from_f95")

for i, sid in enumerate(q2_stars["SOURCEID"][:10]):

    ra_offset_arcsec = (
        np.degrees(q2_stars[q2_stars["SOURCEID"] == sid]["RA"][0] - ra) * 3600
    )
    dec_offset_arcsec = (
        np.degrees(q2_stars[q2_stars["SOURCEID"] == sid]["DEC"][0] - dec) * 3600
    )

    print(
        sid,
        f"\nRA offset: {ra_offset_arcsec:.1f}, DEC offset: {dec_offset_arcsec:.2f}\n",
    )

    this_fig = plt.figure(figsize=(16.42, 4.49))
    this_table = full_cleaned_data[full_cleaned_data["SOURCEID"] == sid]
    this_table["JAPERMAG3"][this_table["JAPERMAG3"] < 0] = np.nan
    this_table["HAPERMAG3"][this_table["HAPERMAG3"] < 0] = np.nan
    this_table["KAPERMAG3"][this_table["KAPERMAG3"] < 0] = np.nan

    plt.subplot(311)
    plt.errorbar(
        this_table["MEANMJDOBS"],
        this_table["JAPERMAG3"],
        fmt="b.",
        yerr=this_table["JAPERMAG3ERR"],
        ms=3,
    )
    plt.gca().invert_yaxis()  
    plt.ylabel("J")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)
    plt.title(
        f"Closest star #{i} near f95, {np.degrees(q2_stars['distance_from_f95'][i])*60:.1f} arcmin away"
    )

    plt.subplot(312)
    plt.errorbar(
        this_table["MEANMJDOBS"],
        this_table["HAPERMAG3"],
        fmt="g.",
        yerr=this_table["HAPERMAG3ERR"],
        ms=3,
    )
    plt.gca().invert_yaxis()  
    plt.ylabel("H")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.subplot(313)
    plt.errorbar(
        this_table["MEANMJDOBS"],
        this_table["KAPERMAG3"],
        fmt="r.",
        yerr=this_table["KAPERMAG3ERR"],
        ms=3,
    )
    plt.gca().invert_yaxis()  
    plt.ylabel("K")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.xlabel("Modified Julian Date")
    plt.savefig(f"closest_{i}_near_f95.pdf")
    plt.savefig(f"closest_{i}_near_f95.png")
