# coding=utf-8
# 

import unittest2
from dif_reader.reader import readDif, getCurrentDirectory
from os.path import join



class TestReadDifError(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestReadDifError, self).__init__(*args, **kwargs)



	def testError01(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'CL Franklin DIF date missing.xls')
		try:
			readDif(inputFile)
		except:
			pass
		else:
			self.fail('data should have occurred')



	def testError02(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'CL Franklin DIF no date line.xls')
		try:
			readDif(inputFile)
		except:
			pass
		else:
			self.fail('data should have occurred')