"""
Processes our data. It's a script. 

Gets around some issues in ATPY that are really riling me up.

"""


import os

import numpy as np
import atpy
import astropy.io.fits

import night_cleanser

path = os.path.expanduser("~/Dropbox/Bo_Tom/NGC1333/WSERV7/")
datapath = path+'DATA/'

# This is a gross workaround because either WSA or ATpy is not handling fits files correctly.
# So we invoke astropy to load and re-save the table data and save all our souls.
if os.path.isfile(datapath+'fulldata.fits'):
	os.remove(datapath+'fulldata.fits')
predata = astropy.io.fits.open(datapath+"results29_8_14_53_103.fits.gz")
tbdata = predata[1].data
hdu = astropy.io.fits.BinTableHDU(tbdata)
hdu.writeto(datapath+'fulldata.fits')

#data = atpy.Table(path+"DATA/results29_8_14_53_103.fits.gz")
data = atpy.Table(datapath+"fulldata.fits")
data.table_name = 'NGC1333'

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

def save_cleansed_data(clobber=True):

	datalist = [cleansed_data, cleansed_scrubbed_data, cleansed_scrubbed_dusted_data]
	pathlist = ['fdece_graded_clipped0.95.fits', 'fdece_graded_clipped0.95_scrubbed0.1.fits', 'fdece_graded_clipped0.95_scrubbed0.1_dusted0.5.fits']

	for data, path in zip(datalist,pathlist):

		if os.path.isfile(datapath+path) and clobber:
			os.remove(datapath+path)
		data.write(datapath+path)

	# cleansed_data.write(datapath+'fdece_graded_clipped0.95.fits')			
	# cleansed_scrubbed_data.write(datapath+'fdece_graded_clipped0.95_scrubbed0.1.fits')
	# cleansed_scrubbed_dusted_data.write(datapath+'fdece_graded_clipped0.95_scrubbed0.1_dusted0.5.fits')