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
    name_col = 'preliminary_ID')

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
    data = atpy.Table(dpath+'Scholz_vizier_votable.vot', tid=2, verbose=False),
    alias = "Scho09",
    full_name = "'Previously confirmed very low mass members in NGC 1333, Table 4 from 2012ApJ...744....6S'",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'ID')
tables.append(Scholz_2009)
Scholz_2012a = TableParameters(
    data = atpy.Table(dpath+'Scholz_vizier_votable.vot', tid=0, verbose=False),
    alias = "Scho12a",
    full_name = "New very low mass members in NGC 1333, Table 2 from 2012ApJ...744....6S",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'SONYC')
tables.append(Scholz_2012a)
Scholz_2012b = TableParameters(
    data = atpy.Table(dpath+'Scholz_vizier_votable.vot', tid=1, verbose=False),
    alias = "Scho12b",
    full_name = "New very low mass members of NGC 1333, Table 1 from 2012ApJ...756...24S",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'SONYC')
tables.append(Scholz_2012b)

Wilking_2004 = TableParameters(
    data = dpath+'Wilking2004_vizier_votable.vot',
    alias = 'MBO',
    full_name = "'Table 1: Photometry of northern NGC 1333 cluster' from 'NGC 1333 low-mass stars infrared photometry (Wilking+, 2004)'",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'MBO'
    )
tables.append(Wilking_2004)

Getman_2002 = TableParameters(
    data = atpy.Table(dpath+"Getman2002_vizier_votable.vot", tid=0, verbose=False),
    alias = 'ACIS',
    full_name = "'Table 1: ACIS NGC 1333 sources and stellar identifications', from 'Young stellar objects in the NGC 1333 (Getman+, 2002)'",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = '__GFT2002_',
    max_match = 2.0)
tables.append(Getman_2002)

Aspin_1994 = TableParameters(
    data = dpath+"Aspin1994.fits",
    alias = 'ASR',
    full_name = "'Sources in NGC1333-S (tables 1, 2, 3 and 5 of paper)' from 'Near-IR imaging photometry of NGC 1333 (Aspin+ 1994)'",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = 'ASR')
tables.append(Aspin_1994)

Lada_1996 = TableParameters(
    data = dpath+"LadaAL.fits",
    alias = 'LAL',
    full_name = "'Catalogue' from 'JHK photometry of NGC1333 (Lada+, 1996)'",
    ra_cols = ['_RAJ2000'], dec_cols = ['_DEJ2000'],
    radec_fmt = 'decimal_degrees',
    name_col = '__LAL96_'
    )
tables.append(Lada_1996)
    
# Here's our first function, that we'll use just to get things rolling
def test():


    return tablemate_core.tablemater(WUVARS_maxvars_p, [Twomass, Gutermuth_2008, Scholz_2009, Wilking_2004, Getman_2002])
            


def vars_match():
    """ 
    A function that matches our variables table to all the other tables!

    Takes about 15 seconds (2/13/13).
    """

    return tablemate_core.tablemater( WUVARS_maxvars_p, tables)

def merge_scholz_columns(matched_table):
    """
    Takes in a table with 3 Scholz columns and merges them into one Scholz column.

    """

    pk = matched_table.columns.keys[0]
    matched_table_copy = matched_table.where(matched_table[pk] == matched_table[pk])

    scholz_a = matched_table['Scho09_ID']
    scholz_b = matched_table['Scho12a_ID']
    scholz_c = matched_table['Scho12b_ID']    

    for i in range(len(scholz_a)):
        if scholz_a[i] == '-1' and scholz_b[i] != '-1':
            scholz_a[i] = scholz_b[i]
        elif scholz_a[i] == '-1' and scholz_c[i] != '-1':
            scholz_a[i] = scholz_c[i]

    matched_table_copy.remove_columns(['Scho09_ID', 'Scho12a_ID', 'Scho12b_ID'])
    matched_table_copy.add_column(name='Scholz_ID', data=scholz_a, after='SpYSO_index')

    return matched_table_copy

