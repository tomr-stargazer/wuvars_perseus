"""
Processes our data. It's a script. 

Gets around some issues in ATPY that are really riling me up.

"""

from __future__ import division
import os

import numpy as np
import atpy

import night_cleanser

path = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/")

data = atpy.Table(path+"DATA/results29_8_14_53_103.fits.gz")
data.table_name = 'NGC133'

# created using variability_script_perseus
spreadsheet = atpy.Table(path+"DATA/spreadsheet/full_data_errorcorrected_ce_spreadsheet.fits")
minimum = spreadsheet.where((spreadsheet.N_j >= 50) |
                            (spreadsheet.N_k >= 50) |
                            (spreadsheet.N_h >= 50) )

s = 0.021                                                  
c = 1.082                                                  
                                                           
data.JAPERMAG3ERR = np.sqrt( c*data.JAPERMAG3ERR**2 + s**2)
data.HAPERMAG3ERR = np.sqrt( c*data.HAPERMAG3ERR**2 + s**2)
data.KAPERMAG3ERR = np.sqrt( c*data.KAPERMAG3ERR**2 + s**2)
                                                           
data.JMHPNTERR = np.sqrt( c*data.JMHPNTERR**2 + s**2)      
data.HMKPNTERR = np.sqrt( c*data.HMKPNTERR**2 + s**2)

# now it's fdece

# constants was created by taking `minimum`, selecting all stars with j_rmsr, h_rmsr, and k_rmsr less than 0.05,
# and then filtering that by removing everything below the median stetson index.

# minimum_constant = minimum.where( (minimum.j_rmsr < 0.05) & (minimum.h_rmsr < 0.05) & (minimum.k_rmsr < 0.05))
# constants = minimum_constant.where( minimum_constant.Stetson < np.median(minimum_constant.Stetson) )
constants = atpy.Table(path+'cleaning_products/constants_spreadsheet.fits')

# created using variability_map.exposure_grader:
#     jvc = variability_map.exposure_grader(data, constants, 'j', 17)
#     hvc = variability_map.exposure_grader(data, constants, 'h', 16.7)
#     kvc = variability_map.exposure_grader(data, constants, 'k', 16)
# By the way, these take about 2 hours to run.
jvc_ratio = np.loadtxt(path+'cleaning_products/exposure_grader_output/jvc_ratio.txt')
hvc_ratio = np.loadtxt(path+'cleaning_products/exposure_grader_output/hvc_ratio.txt')
kvc_ratio = np.loadtxt(path+'cleaning_products/exposure_grader_output/kvc_ratio.txt')

timestamps = np.sort(list(set(data.MEANMJDOBS)))

cleansed_data = night_cleanser.null_cleanser_grader(data, timestamps, jvc_ratio, hvc_ratio, kvc_ratio, threshold=0.95)

cleansed_scrubbed_data = night_cleanser.selective_flag_scrubber(cleansed_data, minimum)

cleansed_scrubbed_dusted_data = night_cleanser.errorbar_duster(cleansed_scrubbed_data)

comment_string = ['FITSWriter: database:WSERV7v20140528',
	'29/05/14 08:14',
	'SQL Query',
	'select SOURCEID, MEANMJDOBS, s.RA, s.DEC, JMHPNT, JMHPNTERR, HMKPNT,',
	'HMKPNTERR, JAPERMAG3, JAPERMAG3ERR, HAPERMAG3, HAPERMAG3ERR,',
	'KAPERMAG3, KAPERMAG3ERR, JPPERRBITS, HPPERRBITS, KPPERRBITS,',
	'MERGEDCLASS, PSTAR         from WSERV7SourceXSynopticSourceBestMatch',
	'as b, WSERV7SynopticMergeLog as l, WSERV7SynopticSource as s  where',
	'b.synFrameSetID=s.synFrameSetID and b.synSeqNum=s.synSeqNum and',
	'b.synFrameSetID=l.synFrameSetID and   s.RA > 0  order by SOURCEID,',
	'MEANMJDOBS']

assert data.comments == comment_string
assert cleansed_data.comments == comment_string
assert cleansed_scrubbed_data.comments == comment_string
assert cleansed_scrubbed_dusted_data.comments == comment_string

def save_cleansed_data():
	cleansed_data.write(path+data+'fdece_graded_clipped0.95.fits')
	cleansed_scrubbed_data.write(path+data+'fdece_graded_clipped0.95_scrubbed0.1.fits')
	cleansed_scrubbed_dusted_data.write(path+data+'fdece_graded_clipped0.95_scrubbed0.1_dusted0.5.fits')