"""
It's a script to export the data from f89, f95 into a format that Ben could use.

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

if __name__ == "__main__":

    # I wish I'd prototyped in Jupyter...

    # read in the data
    f95_table = tab.Table.read("f95_data_for_Ben.fits")
    f89_table = tab.Table.read("f89_data_for_Ben.fits")

    # first, f95

    f95_fig = plt.figure(figsize=(16.42,  4.49))

    plt.subplot(311)
    plt.plot(f95_table["MEANMJDOBS"], f95_table["JAPERMAG3"], "b.", ms=3)
    plt.ylim(16.7, 16)
    plt.ylabel("J")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.subplot(312)
    plt.plot(f95_table["MEANMJDOBS"], f95_table["HAPERMAG3"], "g.", ms=3)
    plt.ylim(14.6, 14.1)
    plt.ylabel("H")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.subplot(313)
    plt.plot(f95_table["MEANMJDOBS"], f95_table["KAPERMAG3"], "r.", ms=3)
    plt.ylim(13.2, 12.7)
    plt.ylabel("K")
    plt.axvline(56201, alpha=0.33)
    plt.axvline(56357, alpha=0.33)

    plt.xlabel("Modified Julian Date")
    plt.savefig("fig_f95_for_Ben.pdf")
    plt.savefig("fig_f95_for_Ben.png")

    # read in the data

    # next, f89, which never has J data.

    f89_fig = plt.figure(figsize=(13.65,  3.09))

    plt.subplot(211)
    plt.plot(f89_table["MEANMJDOBS"], f89_table["HAPERMAG3"], "g.", ms=3)
    plt.ylim(15, 12)
    plt.ylabel("H")

    plt.subplot(212)
    plt.plot(f89_table["MEANMJDOBS"], f89_table["KAPERMAG3"], "r.", ms=3)
    plt.ylim(11.2, 8.7)
    plt.ylabel("K")

    plt.xlabel("Modified Julian Date")
    plt.savefig("fig_f89_for_Ben.pdf", bbox_inches='tight')
    plt.savefig("fig_f89_for_Ben.png", bbox_inches='tight')
