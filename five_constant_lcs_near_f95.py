"""
Bo has asked for five "constant" light-curves near f95 so that we can demonstrate
that the dips in f95's light-curve is not due to data artifacts or anything.
(I'm not honestly worried about that being a problem, but we like to be thorough.)

"""

# we want just the J, H, K, time, and color columns.

import os
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


f89_id = 44508746118971
f95_id = 44508746116800

f89_stardata = NGC1333StarData(photometry_data, f89_id)
f95_stardata = NGC1333StarData(photometry_data, f95_id)

labels = ["f89", "f95"]
stardatas = [f89_stardata, f95_stardata]

colnames = [
    "MEANMJDOBS",
    "JAPERMAG3",
    "JAPERMAG3ERR",
    "HAPERMAG3",
    "HAPERMAG3ERR",
    "KAPERMAG3",
    "KAPERMAG3ERR",
    "JMHPNT",
    "JMHPNTERR",
    "HMKPNT",
    "HMKPNTERR",
]

for label, stardata in zip(labels, stardatas):

    # gather the data and export it

    nt = tab.Table(stardata.s_table.data)
    newer_table = tab.Table([nt[colname] for colname in colnames])
    newer_table.write(f"{label}_data_for_Ben.fits", overwrite=True)
    newer_table.write(f"{label}_data_for_Ben.txt", format="ascii.ipac", overwrite=True)

# second part:
# plotting!