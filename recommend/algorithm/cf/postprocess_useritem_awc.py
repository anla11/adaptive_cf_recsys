'''
	__author__: anlnt2
'''

import pandas as pd
import numpy as np
import time
import datetime
import re
import gc
import os

from lib.utils.indexprocess_lib import conv_tonum, convert_useraslist_tomatrix, convert_itemtomatrix, convert_todf, mapping_id, convert_useraslist_toweightmatrix
from configuration.algorithm_config.cf_algconfig import NTOP, RECOMMEND_MEMORY_SIZE, WRITE_MEMORY_SIZE
# from lib.utils.cudalib import matmul_cuda

def recommend_bymatrix(userhistory_aslist, item_arr, container_size = RECOMMEND_MEMORY_SIZE):   
	n_items, n_users = item_arr.shape[1], len(userhistory_aslist)
	n_container = int((n_users - 1)/container_size+1)
	rec_matrix = np.empty((n_users, item_arr.shape[0])).astype(float)
	user_idx = np.empty(n_users).astype(int)

	print (rec_matrix.shape)
	for i in range(n_container):
		# user_idx_i, user_arr_i = convert_useraslist_tomatrix(userhistory_aslist, n_items)
		user_idx_i, user_arr_i = convert_useraslist_toweightmatrix(userhistory_aslist, n_items)		
		from_idx, to_idx = i * container_size, min((i+1)*container_size, n_users)    
		rec_matrix[from_idx:to_idx] = np.dot(user_arr_i, item_arr.T)
		# rec_matrix[from_idx:to_idx] = matmul_cuda(user_arr_i, item_arr.T)
		user_idx[from_idx:to_idx] = user_idx_i
	return rec_matrix, user_idx

def recommend(userhistory_aslist, itemmatrix_df, mapping_dfs, output_path, container_size = WRITE_MEMORY_SIZE, written_containers = 0):
	user_mapping, item_mapping = mapping_dfs
	n_items, n_users = len(item_mapping), len(userhistory_aslist)
	print (n_users, n_items)
	
	item_idx, item_arr = convert_itemtomatrix(itemmatrix_df, n_items) # itemrec * itemhis
	n_container = int((n_users - 1)/container_size+1)
	for container_idx in range(n_container):
		i = container_idx + written_containers
		from_idx, to_idx = container_idx * container_size, min((container_idx+1)*container_size, n_users)    

		#recommend in container
		start = time.time()
		print ('Container %d: %d-%d' % (container_idx, from_idx, to_idx))
		rec_matrix_i, user_idx_i = recommend_bymatrix(userhistory_aslist.iloc[from_idx:to_idx], item_arr, container_size)
		rec_df_i = convert_todf(rec_matrix_i, user_idx_i, item_idx, NTOP)
		del rec_matrix_i
		del user_idx_i
		gc.collect()
		
		#convert from idx to id
		rec_df_i['item_id'] = mapping_id(rec_df_i['item_idx'], item_mapping)
		rec_df_i['user_id'] = mapping_id(rec_df_i['user_idx'], user_mapping)
		rec_df_i.rename(columns = {'item_id':'rec_id'}, inplace = True)	

		#scale score
		vmin, vmax = np.min(rec_df_i['score']), np.max(rec_df_i['score'])
		rec_df_i['score'] = (rec_df_i['score'] - vmin) / (vmax - vmin)
		
		#write file
		if os.path.exists('%s.csv' % output_path) == False:
			rec_df_i[['user_id', 'rec_id', 'score']].to_csv('%s_00.csv' % (output_path), index = False)
		else:
			with open('%s.csv' % output_path, 'a') as f:
				rec_df_i[['user_id', 'rec_id', 'score']].to_csv('%s_00.csv' % output_path, header=False, mode = 'a', index = False)
		# rec_df_i.to_csv('%s_%02d.csv' % (output_path, i), index = False)
		del rec_df_i
		gc.collect()
		print (time.time() - start)

	del item_arr
	del item_idx
	gc.collect()
	written_containers = n_container
	return written_containers


def read_itemmatrix(itemmatrix_filename, item_mapping):
	itemmatrix_df = pd.read_csv(itemmatrix_filename, dtype = str)
	itemmatrix_df['item_rec'] = conv_tonum(itemmatrix_df['rec_id'], item_mapping)
	itemmatrix_df['item_his'] = conv_tonum(itemmatrix_df['item_id'], item_mapping)
	return itemmatrix_df
