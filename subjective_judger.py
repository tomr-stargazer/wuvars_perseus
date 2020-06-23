"""
Judges the subjective stars.

"""



import numpy as np
from perseus_star_counter import *
from clonekiller import clone_hunterkiller

# Copy/pasted from the google spreadsheet. Wish there were a better way to sync this.
hi_subj_nonpers_comments = [
	'junk',
	'LAIV',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'long term K drift',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'LAIV',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'LAIV + LTD',
	'junk',
	'junk',
	'large amplitude SMOOTH long term variability',
	'large amplitude SMOOTH long term variability',
	'junk',
	'junk',
	'junk',
	'junk',
	'large amplitude SMOOTH long term variability',
	'long term irregular',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'BEAUTIFUL dipper',
	'junk',
	'saturated',
	'messy long term trend',
	'junk',
	'irregular',
	'junk',
	'junk',
	'brightening events',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'VERY RED SMOOTH HIGH AMPLITUDE VARIABLE LONG TERM',
	'junk',
	'junk',
	'junk',
	'long term drift',
	'long term drift',
	'long teerm drift',
	'messy irregular',
	'long term drift (K poss. saturated)',
	'junk',
	'LAIV',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'very good long term drift',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'LAIV; close visual binary (barely resolved)',
	'junk',
	'junk',
	'junk',
	'smooth K variability low amplitude long term',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'junk',
	'long term trend',
	'junk',
	'junk',
	'some long term variability (looks like a distant background O/B star?)',
	'junk']

confirmed_hi_subj_nonpers = hi_subj_nonpers.where(np.array(hi_subj_nonpers_comments) != 'junk')

hi_subj_periods_comments = [
	'EB',
	'junk but hints of a weak EB at 2.1 days',
	'spot',
	'spot',
	'large amplitude spot',
	'junk but hints of a weak EB at 2.1 days',
	'weak spot',
	'spot (messy)',
	'junk',
	'junk',
	'very saturated, all data flagged, possible Periodic Brightening Source',
	'spot',
	'cyclic long term variable P~56d',
	'spot',
	'AA Tau (messy)',
	'CLONE of 283',
	'believable long term trend, fishy J period',
	'PERIODIC BRIGHTENING SOURCE',
	'long term semi cyclic YSO variability (extremely messy AA Tau?)',
	'spot',
	'spot',
	'large amplitude irregular, cyclic with P~58 days, AA Tau color variability',
	'spot',
	'spot',
	'EB, P=1.036',
	'spot, saturated at H&K',
	'EB, P=0.678d',
	'Pulsator, P~4.15 hours']

confirmed_hi_subj_periods = hi_subj_periods.where(np.array(hi_subj_periods_comments) != 'junk')

low_subj_periods_comments = [
	'spot, S=0.965',
	'junk',
	'junk',
	'spot, S=0.883',
	'spot, S=0.736, Very Low Mass (BD/VLM)',
	'spot, S=0.829',
	'junk',
	'junk',
	'junk',
	'junk',
	'spot, S=0.619 + slight long term drift',
	'spot, S=0.9',
	'messy spot, S=0.875',
	'junk',
	'junk',
	'spot, 11.21 days, S=0.783',
	'spot, S=0.785',
	'boring spot',
	'boring spot',
	'junk']

confirmed_low_subj_periods = low_subj_periods.where(np.array(low_subj_periods_comments) != 'junk')

low_subj_nonpers_keepers = [
	'p171',
	'p301',
	'p302',
	'p382',
	'p418']

confirmed_low_subj_nonpers = low_subj_nonpers.where(np.in1d(low_subj_nonpers.preliminary_ID, np.array(low_subj_nonpers_keepers)))

assert len(confirmed_low_subj_nonpers) == len(low_subj_nonpers_keepers)

# Now let's glue some things together

confirmed_subj_nonpers = confirmed_hi_subj_nonpers.where(confirmed_hi_subj_nonpers.RA > 0)
confirmed_subj_nonpers.append(confirmed_low_subj_nonpers)

confirmed_subj_periods = confirmed_hi_subj_periods.where(confirmed_hi_subj_periods.RA > 0)
confirmed_subj_periods.append(confirmed_low_subj_periods)

q0_variables = maxvars.where(np.in1d(maxvars.SOURCEID, confirmed_subj_nonpers.SOURCEID) | 
	                         np.in1d(maxvars.SOURCEID, confirmed_subj_periods.SOURCEID) )

allvars = q2_variables.where(q2_variables.RA > 0)
allvars.append(q1_variables)
allvars.append(q0_variables)

# Systematically remove clones
allvars = clone_hunterkiller(allvars)
q2_variables = allvars.where(np.in1d(allvars.SOURCEID, q2_variables.SOURCEID))
q1_variables = allvars.where(np.in1d(allvars.SOURCEID, q1_variables.SOURCEID))
q0_variables = allvars.where(np.in1d(allvars.SOURCEID, q0_variables.SOURCEID))

'''# append a 'temporary ID' column to allvars!
temporary_ID_column = ['t{0}'.format(x+1) for x in range(len(allvars))] 

allvars.sort('RA')
allvars.add_column(name='temporary_ID', data=temporary_ID_column)
'''

# append a 'final ID' column to allvars!
final_ID_column = ['f{0}'.format(x+1) for x in range(len(allvars))] 

allvars.sort('RA')
allvars.add_column(name='final_ID', data=final_ID_column)


# Repeating much of the logic from before
allvars_periodics = allvars.where( 
    np.in1d(allvars.SOURCEID, periodics.SOURCEID) )

allvars_periods = maxvars_periods.where( 
    np.in1d(maxvars_periods.SOURCEID, allvars_periodics.SOURCEID))

assert (allvars_periods.RA == allvars_periodics.RA).all()
'''allvars_periods.add_column(name='temporary_ID', data=allvars_periodics.temporary_ID)
'''

allvars_periods.add_column(name='final_ID', data=allvars_periodics.final_ID)

# Update the columns in these periodic guys
q1_vars_periods = allvars_periods.where( 
    np.in1d(allvars_periods.SOURCEID, q1_variables.SOURCEID))

q2_vars_periods = allvars_periods.where( 
    np.in1d(allvars_periods.SOURCEID, q2_variables.SOURCEID))

q0_vars_periods = allvars_periods.where( 
    np.in1d(allvars_periods.SOURCEID, q0_variables.SOURCEID))


q1_vars_nonpers = allvars.where(
	np.in1d(allvars.SOURCEID, q1_vars_nonpers.SOURCEID))

q2_vars_nonpers = allvars.where(
	np.in1d(allvars.SOURCEID, q2_vars_nonpers.SOURCEID))

q0_vars_nonpers = q0_variables.where(
    ~np.in1d(q0_variables.SOURCEID, q0_vars_periods.SOURCEID))
q0_vars_nonpers = allvars.where(
    np.in1d(allvars.SOURCEID, q0_vars_nonpers.SOURCEID))

def save_allvars_to_file():

    dropbox_bo_aux = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/aux_catalogs/")
    allvars.write(dropbox_bo_aux+"allvars_spread_with_final_IDs.fits")


