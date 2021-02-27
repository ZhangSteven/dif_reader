# coding=utf-8
#
# Read DIF valuation report from CL trustee and get certain
# numbers out of it.
# 
from xlrd import open_workbook
from toolz.functoolz import compose
from steven_utils.excel import worksheetToLines, fromExcelOrdinal
from steven_utils.iter import firstOf
from functools import partial
from os.path import dirname, abspath
import logging
logger = logging.getLogger(__name__)



getCurrentDirectory = lambda : dirname(abspath(__file__))



def readDif(file):
	"""
	[String] file => 
		( [String] date (yyyy-mm-dd)
		, [Float] total number of units
		, [Float] NAV after fees
		, [Float] Expense
		, [Float] NAV per unit before fees
		, [Float] NAV per unit after fees
		)
	"""
	logger.debug('readDif(): {0}'.format(file))
	return compose(
		lambda lines: \
			( getValuationDate(lines)
			, getNumOfUnits(lines)
			, getNavAfterFee(lines)
			, getExpense(lines)
			, *getNavPerUnit(lines)
			)
	  , list
	  , fileToLines
	)(file)



def checkNotNone(msg, x):
	if x == None:
		logger.error(msg)
		raise ValueError
	else:
		return x



def getExpense(lines):
	"""
	[Iterable] lines => [Float] total number of units
	"""
	logger.debug('getExpense()')
	return getNumberFromTargetLine('Expenses', lines)



def getNumOfUnits(lines):
	"""
	[Iterable] lines => [Float] total number of units
	"""
	logger.debug('getNumOfUnits()')
	return getNumberFromTargetLine('Total Units Held at this Valuation  Date', lines)



def getNavAfterFee(lines):
	"""
	[Iterable] lines => [Float] NAV after fees
	"""
	logger.debug('getNavAfterFee()')
	return getNumberFromTargetLine('Net Asset Value', lines)



def getNavPerUnit(lines):
	"""
	[Iterable] lines => ( [Float] NAV per unit before fee
						, [Float] NAV per unit after fee)
	"""
	logger.debug('getNavPerUnit()')
	linesIter = iter(lines)
	return ( getNumberFromTargetLine('Unit Price', linesIter)
		   , getNumberFromTargetLine('Unit Price', linesIter))



"""
	[String] startingString, [Iterable] lines
		=> [Float] number

	Search for the line whose first cell starts with the startingString, if
	found, then return the first float number in following items of the line.
"""
getNumberFromTargetLine = compose(
	partial(checkNotNone, 'getNumberFromTargetLine(): could not find number')
  , partial(firstOf, lambda x: isinstance(x, float))
  , lambda line: line[1:]
  , partial(checkNotNone, 'getNumberFromTargetLine(): could not find line')
  , lambda startingString, lines: \
  		firstOf( lambda line: \
  					len(line) > 1 and isinstance(line[0], str) and line[0].startswith(startingString)
  			   , lines
  			   )
)



def getValuationDate(lines):
	"""
	[Iterable] lines => [String] date (yyyy-mm-dd)
	"""
	def toDatetime(dt):
		""" [Float] dt => [Datetime] dt """
		try:
			return fromExcelOrdinal(dt)
		except:
			logger.error('getValuationDate(): invalid date {0}'.format(dt))
			raise ValueError


	return compose(
		lambda dt: dt.strftime('%Y-%m-%d')
	  , toDatetime
	  , lambda line: line[3]
	  , partial(checkNotNone, 'getValuationDate(): could not find valuation line')
	  , partial(firstOf, lambda line: len(line) > 3 and line[0].startswith('Valuation Period : From'))
	)(lines)





# [String] file => [Iterable] ([List]) lines
fileToLines = compose(
	worksheetToLines
  , lambda file: open_workbook(file).sheet_by_name('Portfolio Sum.')
)




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	import argparse
	parser = argparse.ArgumentParser(description='Read DIF file for NAV information')
	parser.add_argument('file', metavar='file', type=str, help='input file')

	"""
		To test the program, put a DIF file in the local directory, then:

		$ python dif_reader.py <file name>
	"""
	compose(
		print
	  , readDif
	)(parser.parse_args().file)
