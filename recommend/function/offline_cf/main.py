'''
	__author__: anlnt2
'''

import sys, getopt
from recommend.function.offline_cf.offline_preprocess_cf import run as pre_process
from recommend.function.offline_cf.offline_postprocess_itemmatrix_awc import run as postprocess_itemmatrix
from recommend.function.offline_cf.offline_postprocess_useritem_awc import run as postprocess_useritem
from recommend.function.offline_cf.offline_evaluation_properties import run as evaluate
from recommend.function.offline_cf.offline_test import run as test


def 	run(mode, outputpath, tmppath, hispath, testpath, typestr, param):
# 	print (mode)
	if mode == "preprocess":
		pre_process(tmppath, hispath, typestr) 
	else:
		if mode == 'itemmatrix':
			postprocess_itemmatrix(outputpath, tmppath, typestr)
		elif mode == 'recommend':
			postprocess_useritem(outputpath, tmppath, hispath, typestr)
		elif mode == 'evaluate':
			evaluate(outputpath, tmppath, typestr, param)
		elif mode == 'test':
			test(outputpath, tmppath, hispath, testpath, typestr, param)

def main(argv):
	mode, outputpath, tmppath, hispath, testpath, typestr, param = None, None, None, None, None, None, None
	try:
		opts, args = getopt.getopt(argv,"",["mode=","outputpath=","tmppath=", "train=", "test=", "param=", "type="])
	except getopt.GetoptError:
		print ('Wrong command!')
		print ('main.py --mode --outputpath --tmppath --train --test --param --type')
		sys.exit(2)
	for opt, arg in opts:
		if opt in('--mode'):
			mode = arg
		elif opt in ("--outputpath"):
			outputpath = arg
		elif opt in ("--tmppath"):
			tmppath = arg
		elif opt in ("--train"):
			hispath = arg			
		elif opt in ("--test"):
			testpath = arg			
		elif opt in ("--param"):
			param = arg
		elif opt in ("--type"):
			typestr = arg
	run(mode, outputpath, tmppath, hispath, testpath, typestr, param)

if __name__ == "__main__":
	main(sys.argv[1:])