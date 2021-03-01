# coding=utf-8
#
# Read DIF files from a directory and output their valuation
# information to a csv file.
# 
from dif_reader.reader import readDif
from steven_utils.file import getFiles, getFilenameWithoutPath
from steven_utils.utility import writeCsv
from toolz.functoolz import compose
from functools import partial
import logging
logger = logging.getLogger(__name__)



def showFilesWithError(resultList):
	"""
	[List] resultList => [List] result list

	find out those files whose result is empty, print them out.
	"""
	for r in filter(lambda r: r[1] == (), resultList):
		print('error: {0}'.format(getFilenameWithoutPath(r[0])))

	return resultList



def getDifData(file):
	"""
	[String] file => [Tuple] result

	This function does not throw exception, if anything goes wrong, it will
	return an empty tuple.
	"""
	try:
		return (file, readDif(file))
	except:
		return (file, ())



def writeOutputCsv(file, results):
	"""
	[Iterable] ([Tuple] (date, number of units, ...))
		=> [String] output csv file

	Side effect: write an output csv file
	"""
	return writeCsv(file, results, delimiter=',')




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	import argparse
	parser = argparse.ArgumentParser(description='Read DIF files from a directory')
	parser.add_argument('directory', metavar='directory', type=str, help='input directory')

	"""
		To test the program, put DIF files into a directory and run:

		$ python worker.py <input directory>
	"""
	compose(
		print
	  , partial(writeOutputCsv, 'output.csv')
	  , partial(filter, lambda x: x != ())
	  , partial(map, lambda r: r[1])
	  , showFilesWithError
	  , list
	  , partial(map, getDifData)
	  , lambda directory: getFiles(directory, True)
	)(parser.parse_args().directory)