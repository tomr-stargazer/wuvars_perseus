"""
This is a script (not a module) that counts different types of
stars in my dataset using a self-consistent, editable, referenceable 
set of filters.

Useful importable variable names:
==Global==
 `autovars_true`: all automatically detected variables
 `autovars_strict`: all pristine auto-variables (a subset of `autovars_true`)
==Periodics==
 `autovars_true_periodics`: subset of `autovars_true` who are periodic
 `autovars_true_periods`: same as above, but only when we need their periods
 `autovars_strict_periodics`: subset of `autovars_strict` who are periodic
 `autovars_strict_periods`: same as above, but only when we need their periods
==Non-periodic==
 `autovars_true_nonpers`: subset of `autovars_true` who are non-periodic
 `autovars_strict_nonpers`: subset of `autovars_strict` who are non-periodic

""" 

from __future__ import division
import os

import numpy as np

import atpy

import periodic_selector as ps

def c_print(str):
    if __name__ == '__main__':
        print str
    else:
        pass
    return

dropbox_bo_data = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/DATA/")
dropbox_bo_spread = dropbox_bo_data+'spreadsheet/'

#spread = atpy.Table("/home/tom/reu/ORION/DATA/fdece_graded_clipped0.8_scrubbed0.1_dusted0.5_spread.fits")
spread = atpy.Table(dropbox_bo_spread+"fdece_graded_clipped0.95_scrubbed0.1_dusted0.5_spread.fits")

maxvars_spread_per = atpy.Table(dropbox_bo_spread+"low_maxvars_photometry_aboveStetson0.5_spread.fits")

# Number of detected sources in the dataset
c_print( "Number of detected sources in the dataset:" )
c_print( len(spread) )

# Stars with valid data (that could be considered candidates for inclusion)
# Criteria:
#  At least 50 observations (as measured by Stetson_N or just per band)
#  

minimum = spread.where((spread.N_j >= 50) |
                       (spread.N_k >= 50) |
                       (spread.N_h >= 50) )

q0_stars = minimum

c_print( "Number of stars that meet absolute minimum considerations for valid data:" )
c_print( "(i.e., have at least 50 recorded observations in at least one band)" )
c_print( len(minimum) )

# Automatic variables
# Criteria:
#  At least one band must meet all of the following:
#  -At least 50 detections, less than 200
#  -Brightness between limits (11<K<16, 11<H<16, 11<J<17)
#  -No error flags at all (i.e. N_"info" = 0; severe stuff gets clipped anyway) 
#  AND Stetson value >= 1.
#  -Small caveat: if Stetson value dominated by disqualified bands,
#   observed RMS in a good band must > noise.

sp = spread

maxvars = sp.where( (sp.Stetson > 0.5) & (
        (sp.N_j >= 50) |
        (sp.N_k >= 50) |
        (sp.N_h >= 50) ) )
c_print( "Maximum possible number of variables (Stetson > 0.5) : %d" % len(maxvars) )

# append a 'preliminary ID' column to maxvars!
preliminary_ID_column = ['p{0}'.format(x+1) for x in range(len(maxvars))] 

maxvars.sort('RA')
maxvars.add_column(name='preliminary_ID', data=preliminary_ID_column)

# "True" variability criterion has two cases:
# 1. All 3 bands are quality, and S > 1 (this is identical to CygOB7), or
# 2. 1 or 2 bands is quality and has reduced chisq > 1, and S > 1 just in case.

# "Quality" is as defined above.

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality; S > 1. Note "&"s uniform throughout.
case1 = ( (maxvars.Stetson > 1) & (maxvars.pstar_median > 0.75) &
          (
        (maxvars.N_j >= 50) & (maxvars.N_j <= 135) &    # J band criteria
        (maxvars.j_mean > 11) & (maxvars.j_mean < 17) & 
        (maxvars.N_j_info == 0) 
        ) &
          (
        (maxvars.N_h >= 50) & (maxvars.N_h <= 130) &    # H band criteria
        (maxvars.h_mean > 11) & (maxvars.h_mean < 16.7) & 
        (maxvars.N_h_info == 0) 
        ) &
          (
        (maxvars.N_k >= 50) & (maxvars.N_k <= 150) &    # K band criteria
        (maxvars.k_mean > 11) & (maxvars.k_mean < 16) & 
        (maxvars.N_k_info == 0)
        ) )

# Case 2: at least one band quality and rchi^2 > 1; S > 1. Note mixed "&"s 
# and "|"s, as well as another layer of parentheses around the complex of "|"
# criteria.
case2 = ( ((maxvars.Stetson > 1) & (maxvars.pstar_median > 0.75)) & (
          (
        (maxvars.N_j >= 50) & (maxvars.N_j <= 135) &    # J band criteria
        (maxvars.j_mean > 11) & (maxvars.j_mean < 17) & 
        (maxvars.N_j_info == 0) & (maxvars.j_rchi2 > 1) 
        ) |
          (
        (maxvars.N_h >= 50) & (maxvars.N_h <= 130) &    # H band criteria
        (maxvars.h_mean > 11) & (maxvars.h_mean < 16.7) & 
        (maxvars.N_h_info == 0) & (maxvars.h_rchi2 > 1) 
        ) |
          (
        (maxvars.N_k >= 50) & (maxvars.N_k <= 150) &    # K band criteria
        (maxvars.k_mean > 11) & (maxvars.k_mean < 16) & 
        (maxvars.N_k_info == 0) & (maxvars.k_rchi2 > 1) 
        ) ) )

autovars_true = maxvars.where( case1 | case2 )

autovars_strict = maxvars.where( case1 )

q2_variables = autovars_strict
q1_variables = autovars_true.where(~np.in1d(autovars_true.SOURCEID, q2_variables.SOURCEID))
assert q1_variables.SOURCEID[0] not in q2_variables.SOURCEID
assert q2_variables.SOURCEID[0] not in q1_variables.SOURCEID


# Now, to count how many stars have quality that meets "autovars_true".

# Constructing these as two separate arrays for ease of reading/editing.
# Case 1: all 3 bands are quality. Note "&"s uniform throughout.
cand_case1 = ( (sp.pstar_median > 0.75) & ( 
        (sp.N_j >= 50) & (sp.N_j <= 135) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) 
        ) &
          (
        (sp.N_h >= 50) & (sp.N_h <= 130) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16.7) & 
        (sp.N_h_info == 0) 
        ) &
          (
        (sp.N_k >= 50) & (sp.N_k <= 150) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0)
        ) )

# Case 2: at least one band quality. Note mixed "&"s and "|"s, 
# as well as another layer of parentheses around the complex of "|" criteria.
cand_case2 = ( (sp.pstar_median > 0.75) & (
    (
        (sp.N_j >= 50) & (sp.N_j <= 135) &    # J band criteria
        (sp.j_mean > 11) & (sp.j_mean < 17) & 
        (sp.N_j_info == 0) 
        ) |
    (
        (sp.N_h >= 50) & (sp.N_h <= 130) &    # H band criteria
        (sp.h_mean > 11) & (sp.h_mean < 16.7) & 
        (sp.N_h_info == 0) 
        ) |
    (
        (sp.N_k >= 50) & (sp.N_k <= 150) &    # K band criteria
        (sp.k_mean > 11) & (sp.k_mean < 16) & 
        (sp.N_k_info == 0) 
        ) ) )


autocan_true = sp.where( cand_case1 | cand_case2 )
autocan_strict = sp.where( cand_case1 )

q2_stars = autocan_strict
q1_stars = autocan_true.where(~np.in1d(autocan_true.SOURCEID, q2_stars.SOURCEID))
assert q1_stars.SOURCEID[0] not in q2_stars.SOURCEID
assert q2_stars.SOURCEID[0] not in q1_stars.SOURCEID


c_print( "Number of stars automatically classed as variables: %d" % len(autovars_true) )
c_print( "Number of stars that have the data quality for auto-classification: %d" % len(autocan_true) )

subjectives = maxvars.where( ~np.in1d(maxvars.SOURCEID, autovars_true.SOURCEID))

c_print( "" )
c_print( "Number of probably-variable stars requiring subjective verification due to imperfect data quality: %d" % len(subjectives) )

# Now let's count stars that meet our strict criteria in ALL 3 bands

c_print( "" )

c_print( "Number of STRICT autovariables: %d" % len(autovars_strict) )
c_print( "Number of STRICT autocandidates: %d" % len(autocan_strict) )

c_print( "" )

c_print( " Q: Statistically, what fraction of our stars are variables?" )
c_print( " A: %.2f%s, drawn from the tightest-controlled sample;" % (len(autovars_strict)/len(autocan_strict) * 100, r"%") )
c_print( "    %.2f%s, drawn from a looser sample." % (len(autovars_true)/len(autocan_true) * 100, r"%") )

# Now for periodicity analysis, which relies on long_periodic_selector

period_override = {
    44508746116800 : 26.42, # periodic brightener
    44508746092968 : 16.283440 / 24, # EBs
    44508746095248 : 1.035867,
    44508746104931 : 10.711130 / 24,
    44508746111818 : 1.672848,
    44508746114638 : 1.713077,
    44508746120939 : 3.154922,
    44508746124658 : 15.198723 / 24,
    44508746127865 : 2.045,
    44508746128156 : 4.035187,
    44508746093223 : 4.155218 / 24, # pulsating stars
    44508746113922 : 13.702932 / 24,
    44508746121910 : 12.926229 / 24,
    44508746105255 : 0.213672930845,
}

# assert that all the overrides are in maxvars!
for key in period_override.keys():
    assert key in maxvars.SOURCEID

periodics = ps.best_long_period(
    ps.long_periodic_selector(maxvars_spread_per, min_period=2, max_period=75, period_override=period_override), 
    min_period=2, max_period=75, period_override=period_override)
periodics.sort('RA')

maxvars_periodics = maxvars.where( 
    np.in1d(maxvars.SOURCEID, periodics.SOURCEID) )

autovars_true_periodics = autovars_true.where( 
    np.in1d(autovars_true.SOURCEID, periodics.SOURCEID) )

autovars_strict_periodics = autovars_strict.where(
    np.in1d(autovars_strict.SOURCEID, periodics.SOURCEID) )


c_print( "" )
c_print( "Number of possible variables with detected periods: %d" % len(maxvars_periodics) )
c_print( "Number of autovariables that are periodic: %d" % len(autovars_true_periodics) )
c_print( "Number of STRICT autovariables that are periodic: %d" % len(autovars_strict_periodics) )
c_print( "Number of possible periodic variables requiring subjective validation: %d" % (len(maxvars_periodics) - len(autovars_true_periodics)) )
c_print( "" )


c_print( " Q: Statistically, what fraction of our variables are periodic?" )
c_print( " A: %.2f%s, drawn from the tightest-controlled sample;" % (len(autovars_strict_periodics)/len(autovars_strict) * 100, r"%") )
c_print( "    %.2f%s, drawn from a looser sample." % (len(autovars_true_periodics)/len(autovars_true) * 100, r"%") )

c_print( "" )
c_print( " Q: What fraction of stars in this dataset are periodic variables?" )
c_print( " A: %.2f%s, drawn from the tightest-controlled sample;" % (len(autovars_strict_periodics)/len(autocan_strict) * 100, r"%") )
c_print( "    %.2f%s, drawn from a looser sample." % (len(autovars_true_periodics)/len(autocan_true) * 100, r"%") )

# The following is only suitable for almost-but-not-quite 
# accurate histogram analysis (because it ditches the s1-only periodocs)

# intersection of periodics and maxvars_periodics
maxvars_periods = periodics.where( 
    np.in1d(periodics.SOURCEID, maxvars_periodics.SOURCEID))

assert (maxvars_periods.RA == maxvars_periodics.RA).all()
maxvars_periods.add_column(name='preliminary_ID', data=maxvars_periodics.preliminary_ID)

# etc
autovars_true_periods = maxvars_periodics.where( 
    np.in1d(maxvars_periodics.SOURCEID, autovars_true_periodics.SOURCEID))

autovars_strict_periods = maxvars_periodics.where( 
    np.in1d(maxvars_periodics.SOURCEID, autovars_strict_periodics.SOURCEID))

#print "hey look i'm here"

## The following creates spreadsheets of nonvariables, as an official reference,
# such that I don't botch anything down the line.

# Nonperiodic autovariables
autovars_true_nonpers = autovars_true.where(
    ~np.in1d(autovars_true.SOURCEID, autovars_true_periodics.SOURCEID))

autovars_strict_nonpers = autovars_strict.where(
    ~np.in1d(autovars_strict.SOURCEID, autovars_strict_periodics.SOURCEID))

q1_vars_periods = maxvars_periods.where( 
    np.in1d(maxvars_periods.SOURCEID, q1_variables.SOURCEID))

q2_vars_periods = maxvars_periods.where( 
    np.in1d(maxvars_periods.SOURCEID, q2_variables.SOURCEID))

assert (q2_vars_periods.preliminary_ID == autovars_strict_periodics.preliminary_ID).all()

q2_vars_nonpers = q2_variables.where(
    ~np.in1d(q2_variables.SOURCEID, q2_vars_periods.SOURCEID))
q1_vars_nonpers = q1_variables.where(
    ~np.in1d(q1_variables.SOURCEID, q1_vars_periods.SOURCEID))

hi_subjectives = subjectives.where(subjectives.Stetson > 1)
hi_subj_periods = maxvars_periods.where(np.in1d(maxvars_periods.SOURCEID, hi_subjectives.SOURCEID))

low_subjectives = subjectives.where(subjectives.Stetson <= 1)
low_subj_periods = maxvars_periods.where(np.in1d(maxvars_periods.SOURCEID, low_subjectives.SOURCEID))

hi_subj_nonpers = hi_subjectives.where(
    ~np.in1d(hi_subjectives.SOURCEID, hi_subj_periods.SOURCEID))
low_subj_nonpers = low_subjectives.where(
    ~np.in1d(low_subjectives.SOURCEID, low_subj_periods.SOURCEID))


assert len(maxvars) == len(q2_vars_periods) + len(q2_vars_nonpers) + len(q1_vars_periods) + len(q1_vars_nonpers) + len(subjectives)
assert len(subjectives) == len(hi_subj_periods) + len(hi_subj_nonpers) + len(low_subj_periods) + len(low_subj_nonpers)

def save_maxvars_to_file():

    dropbox_bo_aux = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/aux_catalogs/")
    maxvars.write(dropbox_bo_aux+"maxvars_spread_with_preliminary_IDs.fits")

eclipsing_binary_SOURCEIDs = [
    44508746092968,
    44508746095248,
    44508746104931,
    44508746111818,
    44508746114638,
    44508746120939,
    44508746124658,
    44508746127865,
    44508746128156]

eclipsing_binaries = maxvars_periods.where(np.in1d(maxvars_periods.SOURCEID, eclipsing_binary_SOURCEIDs))

pulsating_SOURCEIDs = [44508746093223,
    44508746113922,
    44508746121910,
    44508746105255]

pulsators = maxvars_periods.where(np.in1d(maxvars_periods.SOURCEID, pulsating_SOURCEIDs))


