"""
A script that makes lots of light curves.

"""

from __future__ import division
import os

import matplotlib.pyplot as plt

from perseus_star_counter import *

import plot4

dropbox_bo_data = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/DATA/")
photometry_data = atpy.Table('{0}fdece_graded_clipped0.95_scrubbed0.1_dusted0.5.fits'.format(dropbox_bo_data))

# So basically we are relying on the output of perseus_star_counter and saving lightcurves and stuff.

# Let's turn these into functions that take in an input table.

def generate_periodic_lightcurves(spreadsheet, path, name_column='preliminary_ID', test=False):
	assert hasattr(spreadsheet, 'best_period')
	assert hasattr(spreadsheet, name_column)	
	if not path.endswith('/'):
		path += '/'

	# generate stardatas
	sdlist = [plot4.StarData(photometry_data, x, date_offset=56141, name='{0}: {1}'.format(y,x)) for y, x in zip(spreadsheet[name_column], spreadsheet.SOURCEID)]

	for sdx, period in zip(sdlist, spreadsheet.best_period):
		fig = plot4.lc_and_phase_and_colors(sdx, period=period)
		fig.ax_k_lc.set_xlim(0,250)
		fig.ax_j_lc.set_title(sdx.name)
		fig.ax_khk.set_title("S = {0:.3}".format(sdx.Stetson()))

		fig.canvas.draw()
		plt.savefig('{1}{0}.png'.format(sdx.name, path))
		plt.close()
		if test: break

	return path

def generate_nonperiodic_lightcurves(spreadsheet, path, name_column='preliminary_ID', test=False):
	assert hasattr(spreadsheet, name_column)	
	if not path.endswith('/'):
		path += '/'

	sdlist = [plot4.StarData(photometry_data, x, date_offset=56141, name='{0}: {1}'.format(y,x)) for y, x in zip(spreadsheet[name_column], spreadsheet.SOURCEID)]

	for sdx in sdlist:
	    fig = plot4.basic_lc(sdx)
	    fig.ax_k.set_xlim(0,250)
	    fig.ax_j.set_title(sdx.name)
	    fig.ax_khk.set_title("S = {0:.3}".format(sdx.Stetson()))

	    fig.canvas.draw()
	    plt.savefig('{1}{0}.png'.format(sdx.name, path))
	    plt.close()
	    if test: break

	return path

# Which lightcurves do we wanna generate?

lightcurve_path = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/lightcurves/")

def generate_all_lightcurves(test=False):

	# periodics
	periodic_spreadsheets = [q2_vars_periods, q1_vars_periods, hi_subj_periods, low_subj_periods]
	periodic_paths = ['q2/periodic', 'q1/periodic', 'subjective/hi_subjectives/periodic', 'subjective/low_subjectives/periodic']
	periodic_paths = ['{0}{1}'.format(lightcurve_path, x) for x in periodic_paths]

	for spread, path in zip(periodic_spreadsheets, periodic_paths):

		generate_periodic_lightcurves(spread, path, test=test)

	nonperiodic_spreadsheets = [q2_vars_nonpers, q1_vars_nonpers, hi_subj_nonpers, low_subj_nonpers]
	nonperiodic_paths = ['q2/nonperiodic', 'q1/nonperiodic', 'subjective/hi_subjectives/nonperiodic', 'subjective/low_subjectives/nonperiodic']
	nonperiodic_paths = ['{0}{1}'.format(lightcurve_path, x) for x in nonperiodic_paths]

	for spread, path in zip(nonperiodic_spreadsheets, nonperiodic_paths):

		generate_nonperiodic_lightcurves(spread, path, test=test)

	return None


