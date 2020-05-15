'''
	__author__: anlnt2
'''

import pandas as pd
import numpy as np
import gc
import os
import time

def create_itemmatrix(matrix_filepath, output_filepath, preproces_folder):
	'''
		read matrix.txt 
		mapping index with item_id. 
			file contains mapping index_id is preproces_folder/itemcnt.csv
		writing itemmatrix as pandas with id to output_filepath
	'''
	start = time.time()
	data = np.loadtxt(matrix_filepath)
	df = pd.DataFrame({'item_rec':np.array(data[:, 0]).astype(int), 'item_his': np.array(data[:, 1]).astype(int), 'score':data[:, 2]})
	print ('item2item result: ', time.time() - start)

	start = time.time()
	item_cnt = pd.read_csv('%s/itemcnt.csv'%(preproces_folder))
	df = df.merge(item_cnt, left_on = ['item_rec'], right_on = ['item_idx'])
	del df['item_idx']
	df.rename(columns = {'item_id':'rec_id', 'count': 'itemrec_cnt'}, inplace = True)
	df = df.merge(item_cnt, left_on = ['item_his'], right_on = ['item_idx'])
	del df['item_idx']
	df.rename(columns = {'count': 'itemhis_cnt'}, inplace = True)
	print ('Mapping time: ', time.time() - start)
	
	start = time.time()

	df[['item_id', 'rec_id', 'itemhis_cnt', 'itemrec_cnt', 'score']].to_csv(output_filepath, index = False)
	print ('Writing file time: ', time.time() - start)
	gc.collect()