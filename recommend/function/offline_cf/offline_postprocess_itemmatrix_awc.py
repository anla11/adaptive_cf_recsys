'''
	__author__: anlnt2
'''

import pandas as pd
import numpy as np
import gc
import os
import time

from recommend.algorithm.cf.postprocess_itemmatrix_awc import create_itemmatrix

def run(outputpath, tmppath, typestr):
	usergroup = "wide"
	matrix_filepath	= '%s/%s_matrix_%s.txt'%(tmppath, typestr, usergroup)	
	output_filepath = '%s/%s_itemmatrix_%s.csv' % (outputpath, typestr, usergroup)
	create_itemmatrix(matrix_filepath, output_filepath, tmppath)