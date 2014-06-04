"""
Extensions to wuvars-proto/tr/plot4.py that are relevant to NGC1333.

"""

from __future__ import division

from plot4 import StarData

class NGC1333StarData(StarData):
	def __init__(self, table, sid, name=None):
		StarData.__init__(self, table, sid, name=name, date_offset=56141)

