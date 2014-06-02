"""
This is the SCRIPT that mates tables in the NGC1333 catalog,
by calling the MODULE tablemate_core.py.

This should be kept, broadly, in sync with the Google Doc
"Auxiliary Tables in NGC1333".

# change this --
We are asking three broad questions:
1. How many of our variables are previously-known sources?
2. How many of our variables are previously-known variables?
3. How many previously-known variables in this field do we recover?

"""

import os

import numpy as np

import tablemate_core
from tablemate_core import TableParameters, atpy
#import megeath_fulltable_parser_oneoff

# Top half of the script: defining various tables
dpath = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/aux_catalogs/")
tables = []


WUVARS_maxvars_p = TableParameters(
    data = dpath+"maxvars_spread_with_preliminary_IDs.fits",
    alias= "WUVARS_2014_preliminary",
    full_name = "'Master spreadsheet for 647 candidate variables', from 'Near-Infrared Variables in NGC1333', Reipurth & Rice.",
    ra_cols = ['RA'], dec_cols=['DEC'],
    radec_fmt = 'decimal-radians',
    name_col = 'SOURCEID')

Twomass = TableParameters(
    data = dpath+"2MASS_PSC_boxsearch_1degree_NGC1333.tbl",
    alias = "2MASS_PSC",
    full_name = "Two Micron All-Sky Survey: All-Sky Data Release Point Source Catalog. Released 2003 Mar 25. Box search: center (52.20630610 +31.28607228), sidelength 3600 arcsec.",
    ra_cols = ['ra'], dec_cols = ['dec'],
    radec_fmt = 'decimal-degrees',
    name_col = 'designation')
tables.append(Twomass)

Gutermuth_2008 = TableParameters(
    data = dpath+"Gutermuth2008_table2.fits",
    alias = 'SpYSO', 
    full_name = "'Spitzer-identified YSOs: 2MASS, IRAC and MIPS photometries, and addendum (tables 2 and 3 of paper)', from 'SPITZER OBSERVATIONS OF NGC 1333: A STUDY OF STRUCTURE AND EVOLUTION IN A NEARBY EMBEDDED CLUSTER', Gutermuth et al. (2008).",
    ra_cols = ['RAJ2000'], dec_cols = ['DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'Seq')
tables.append(Gutermuth_2008)

# 1.  J/ApJ/744/6/table2  (c)New very low mass members in NGC 1333, Table 2 from 2012ApJ...744....6S (10 rows)
# 2.  J/ApJ/744/6/tablen1 (c)New very low mass members of NGC 1333, Table 1 from 2012ApJ...756...24S (7 rows)
# 3.  J/ApJ/744/6/table4  (c)Previously confirmed very low mass members in NGC 1333, Table 4 from 2012ApJ...744....6S (41 rows)
#    tid=0 : J/ApJ/744/6/table2
#    tid=1 : J/ApJ/744/6/tablen1
#    tid=2 : J/ApJ/744/6/table4
Scholz_2009 = TableParameters(
    data = atpy.Table(dpath+'Scholz_vizier_votable.vot', tid=2),
    alias = "Scho09",
    full_name = "'Previously confirmed very low mass members in NGC 1333, Table 4 from 2012ApJ...744....6S'",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'ID')
Scholz_2012a = TableParameters(
    data = atpy.Table(dpath+'Scholz_vizier_votable.vot', tid=0),
    alias = "Scho12a",
    full_name = "New very low mass members in NGC 1333, Table 2 from 2012ApJ...744....6S",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'SONYC')
Scholz_2012b = TableParameters(
    data = atpy.Table(dpath+'Scholz_vizier_votable.vot', tid=1),
    alias = "Scho12b",
    full_name = "New very low mass members of NGC 1333, Table 1 from 2012ApJ...756...24S",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'SONYC')


    
# Here's our first function, that we'll use just to get things rolling
def test():
    wov = tablemate_core.osc.autovars_strict

    wov_avs = TableParameters(
        #data
        wov,
        #alias
        "WFCAM Orion",
        #full name
        "Strict automatic variables found in the WFCAM Orion monitoring survey. From 'High Amplitude and Periodic Near-Infrared Variables in the Orion Nebula Cluster' by Rice, Thomas S.; Reipurth, Bo; et al.",
        #ra_cols, dec_cols
        ['RA'], ['DEC'],
        #radec_fmt
        'decimal radians',
        #name_col
        'SOURCEID')


    return tablemate_core.tablemater(wov_avs, [
            Herbst2002, YSOVAR_NoExcess, YSOVAR_YSOs, DaRio_2010,
            DaRio_2009, Carpenter_2001, COUP_Getman2005, eso_ha])
            


def vars_match():
    """ 
    A function that matches our variables table to all the other tables!

    Takes about 15 seconds (2/13/13).
    """

    return tablemate_core.tablemater( Rice_2013_vars, tables)

def UKvars_match():
    
    return tablemate_core.tablemater( Rice_UKvars, tables)
