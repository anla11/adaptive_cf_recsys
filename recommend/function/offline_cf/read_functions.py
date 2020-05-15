import numpy as np
import pandas as pd
import os
import gc

from lib.utils.numpyprocess_lib import create_vector

def read_userhis(history_filepath):
	usr_df = None
	if os.path.exists(history_filepath) == False:
		print ('%s not exist' % history_filepath)
	else:
		print ('Read %s' % history_filepath)
		usr_df = pd.read_csv(history_filepath, dtype = str)
	if 'playtime' in usr_df.columns:
		usr_df['playtime'] = np.array(usr_df['playtime']).astype(int)
		usr_df = usr_df[usr_df['playtime'] > 20]
	usr_df.dropna(subset = ['user_id', 'item_id'], inplace = True)        
	return usr_df

def read_his_fullinfo(outputpath, tmppath, hispath, typestr):
	# video_type = read_videotypes(date, hour)
	all_item = pd.read_csv('%s/itemcnt.csv' % (tmppath), dtype = str)
	all_item['item_idx'] = np.array(all_item['item_idx']).astype(int)	

	usr_df = read_userhis('%s' % hispath)
	usr_df = usr_df.merge(all_item, on = ['item_id'])	
	return usr_df, all_item	

def read_objectcnt(tmppath, typestr):
	user_filename = '%s/%s_usercnt.csv' % (tmppath, typestr)
	print ('Reading %s' % user_filename)
	user_cnt = pd.read_csv(user_filename, dtype = str)
	user_cnt['user_idx'] = np.array(user_cnt['user_idx']).astype(int)	
	del user_cnt['count']

	item_filename = '%s/itemcnt.csv' % (tmppath)
	print ('Reading %s' % item_filename)
	item_cnt = pd.read_csv(item_filename, dtype = str)
	item_cnt['count'] = np.array(item_cnt['count']).astype(int)
	item_cnt['item_idx'] = np.array(item_cnt['item_idx']).astype(int)
	n_items = max(item_cnt['item_idx']) + 1
	item_cnt_arr = create_vector(n_items, np.array(item_cnt['item_idx']), np.array(item_cnt['count']))

	return user_cnt, item_cnt, item_cnt_arr, n_items
