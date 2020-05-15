'''
	__author__: anlnt2
'''

import numpy as np
import pandas as pd
import os
import gc
import time

from lib.userhistory_lib.evaluation_lib import *
from recommend.function.offline_cf.read_functions import read_objectcnt
from recommend.function.offline_cf.config import NTOP_REC, NTOP_EVA
n_sample_user = None

def evaluate(output_folder, user_cnt, item_cnt, item_cnt_arr, n_items):
	start = time.time()
	global n_sample_user
	n_sample_user = user_cnt.user_id.nunique()

	nrows = n_sample_user*NTOP_REC
	user_novelty = np.empty((n_sample_user))
	item_reccnt = np.zeros(n_items)
	last_idx = 0
	for i in range(20):
		fi = '%s_%02d.csv' % (output_folder, i)
		print (fi)
		if os.path.exists(fi) == False:
			print ('%s does not exist' % fi)
			break		
		rec_df_i = pd.read_csv(fi, nrows = nrows, dtype = str)
		rec_df_i = rec_df_i.merge(user_cnt, on = ['user_id'])

		if len(rec_df_i) == 0:
			continue
		rec_df_i.rename(columns = {'rec_id':'item_id'}, inplace = True)
		rec_matrix_i = convert_totopmatrix(rec_df_i, item_cnt, NTOP_EVA)
		from_idx = last_idx
		last_idx = from_idx + min(n_sample_user-last_idx, len(rec_matrix_i))
		rec_matrix = rec_matrix_i[:last_idx-from_idx]
		user_novelty[from_idx:last_idx] = cal_user_novelty(rec_matrix, item_cnt_arr)
		item_reccnt = cal_item_reccnt(rec_matrix, n_sample_user, NTOP_EVA, item_reccnt)

		gc.collect()    
		if last_idx >= n_sample_user:
			break
	print (time.time() - start)
	return user_novelty, item_reccnt

def run(output_dir, tmppath, typestr, param = None):
	# print ('Use default group of user: wide')
	output_folder = '%s/%s_awc_useritem' % (output_dir, typestr)		
	user_cnt, item_cnt, item_cnt_arr, n_items = read_objectcnt(tmppath,typestr)
	global n_sample_user
	n_sample_user = user_cnt['user_idx'].nunique()
	print ('Number of users: ', n_sample_user)

	user_novelty, item_reccnt = evaluate(output_folder, user_cnt, item_cnt, item_cnt_arr, n_items)
	novelty = cal_novelty(user_novelty)
	diversity = cal_diversity(item_reccnt, n_sample_user, NTOP_EVA)
	coverage = cal_coverage(item_reccnt)
	congestion = cal_congestion(item_reccnt)
	print (param, '\t', novelty,'\t', diversity, '\t',coverage, '\t',congestion)  
	res = pd.DataFrame({'param':[param], 'popularity':[novelty],\
				'diversity': diversity, 'coverage':coverage, 'congestion':congestion})
	evaluate_filename = None
	evaluate_filename = '%s/%s_evaluate.csv' % (output_dir, typestr)
	res.to_csv(evaluate_filename, index = False)