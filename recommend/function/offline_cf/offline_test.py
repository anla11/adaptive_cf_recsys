'''
	__author__: anlnt2
'''

import pandas as pd
import numpy as np
import os
import gc
from config import NTOP_EVA

def read_testdata(train_path, test_path, itemcnt_path):
	train_df = pd.read_csv(train_path, dtype = str)
	rating = None
	if 'rating' in train_df.columns:
		train_df['rating'] = np.array(train_df['rating']).astype(float)
		rating = train_df.groupby(['item_id'])['rating'].mean().reset_index(name = 'rating')

	item_list = pd.read_csv(itemcnt_path, dtype = str)
	item_list['count'] = np.array(item_list['count']).astype(int)

	test_df = pd.read_csv(test_path, dtype = str)
	test_df = test_df[test_df['item_id'].isin(train_df['item_id'].unique())]

	if 'rating' in test_df.columns:
		del test_df['rating']
	return item_list, rating, test_df

def read_recresult(item_list, rating, test_df, evaluate_path, output_path):
	evaluate_df = pd.read_csv(evaluate_path)
	test_df = test_df[test_df['item_id'].isin(item_list['item_id'])]

	user_df = pd.DataFrame()
	
	for i in range(20):
		fi = '%s_%02d.csv' % (output_path, i)
		if os.path.exists(fi) == False:
			break
		print (fi)
		train_output_i = pd.read_csv(fi, dtype = str)
		train_output_i.rename(columns = {'rec_id':'item_id'}, inplace = True)
		if rating is not None:
			train_output_i = train_output_i.merge(rating, on = ['item_id'], how = 'left')

		train_output_i['score'] = np.array(train_output_i['score']).astype(float)
		train_output_i = train_output_i.sort_values(by = ['user_id', 'score'], ascending = [1, 0])

		both_i = pd.merge(train_output_i, test_df, on = ['user_id', 'item_id'])
		
		user_df_i = both_i.groupby(['user_id'])['item_id'].nunique().reset_index(name = 'user_correctcnt')

		user_rating_i = None
		if rating is not None:
			user_rating_i = both_i.groupby(['user_id'])['rating'].mean().reset_index(name = 'rating')
			user_df_i = user_df_i.merge(user_rating_i, how = 'left')

		user_df_i['user_correctcnt'] = user_df_i['user_correctcnt'].fillna(0)
		user_df_i['precision'] = user_df_i['user_correctcnt'] / NTOP_EVA
		user_df_i['precision'] = user_df_i['user_correctcnt'] / NTOP_EVA
		user_df = pd.concat([user_df, user_df_i])

		del train_output_i
		del user_df_i
		gc.collect()

	evaluate_df['precision'] = [np.mean(user_df['precision'])]
	if rating is not None:
		user_df.dropna(subset = ['rating'], inplace = True)
		evaluate_df['rating'] = [np.mean(user_df['rating'])]
	else:
		evaluate_df['rating'] = 0
	evaluate_df = evaluate_df[['param', 'popularity', 'diversity', 'coverage', 'congestion', 'precision', 'rating']]
	print (evaluate_df)
	evaluate_df.to_csv(evaluate_path, index = False)

def run(output_dir, tmppath, train_path, test_path, typestr, param):
	itemcnt_path = '%s/itemcnt.csv' % (tmppath)
	output_path = '%s/%s_awc_useritem' % (output_dir, typestr)
	evaluate_path = '%s/%s_evaluate.csv' % (output_dir, typestr)
	item_list, rating, test_df = read_testdata(train_path, test_path, itemcnt_path)
	read_recresult(item_list, rating, test_df, evaluate_path, output_path)