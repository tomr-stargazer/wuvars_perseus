"""
This is a oneoff script to facilitate our google spreadsheet thing.

"""

from __future__ import division

import numpy as np

from tablemate_script_perseus import vars_match, merge_scholz_columns
import astrolib.coords as coords

from perseus_star_counter import *

# Take in a table of some kind

match_table = merge_scholz_columns(vars_match())

def output_tab_delineated_spreadsheet(spreadsheet, print_column_headers=False):

	column_headers = [key for key in match_table.columns.keys if 'index' not in key]

	column_headers.insert(1, 'DEC')
	column_headers.insert(1, 'RA')

	return_string = ''
	if print_column_headers:
		for header in column_headers:
			return_string += '{0} \t'.format(header),
		return_string += '\n'

	spreadsheet_matched = match_table.where(np.in1d(match_table.WUVARS_2014_preliminary_ID, spreadsheet.preliminary_ID))

	RA_array = []
	DEC_array = []

	for (ra, dec) in zip(spreadsheet.RA, spreadsheet.DEC):
		pp = coords.Position((ra, dec), units='rad')
		ra_s, de_s = pp.hmsdms().split(' ')
		RA_array.append(ra_s)
		DEC_array.append(' '+de_s)

	primary_header = column_headers[0]


	row_strings = []

	for i in range(len(spreadsheet_matched)):

		row_list = [str(spreadsheet_matched[primary_header][i])]
		row_list.extend([str(RA_array[i]), str(DEC_array[i])])
		row_list.extend([str(spreadsheet_matched[header][i]) for header in column_headers if (header != primary_header) and (len(header) > 3)])

		row_strings.append('\t'.join(row_list))

	return_string += '\n'.join(row_strings)

	return return_string

