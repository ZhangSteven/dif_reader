# coding=utf-8
# 

import unittest2
from dif_reader.reader import readDif, getCurrentDirectory
from os.path import join



class TestDifReader(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestDifReader, self).__init__(*args, **kwargs)



	def testReadDif(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'CL Franklin DIF 2021-02-24.xls')
		result = readDif(inputFile)
		self.assertEqual('2021-02-24', result[0])
		self.assertAlmostEqual(352385999.6876, result[1], 4)
		self.assertAlmostEqual(4700246581.91, result[2], 2)
		self.assertAlmostEqual(-155253.19, result[3], 2)
		self.assertAlmostEqual(13.3382, result[4], 4)
		self.assertAlmostEqual(13.3383, result[5], 4)



	def testReadDif2(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'CL Franklin DIF 2020-02-06 (Revised).xls')
		result = readDif(inputFile)
		self.assertEqual('2020-02-09', result[0])
		self.assertAlmostEqual(383204594.6874, result[1], 4)
		self.assertAlmostEqual(4869895384.64, result[2], 2)
		self.assertAlmostEqual(-227422.14, result[3], 2)
		self.assertAlmostEqual(12.7082, result[4], 4)
		self.assertAlmostEqual(12.7083, result[5], 4)