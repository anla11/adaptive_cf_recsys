'''
	__author__: anlnt2
'''

import numpy as np
import pandas as pd
import os
import datetime
import time
from lib.utils.indexprocess_lib import create_index, get_iteminfo, get_usrhis_byindex
from configuration.algorithm_config.cf_algconfig import GRAPH_FEATURE
from recommend.function.offline_cf.read_functions import read_userhis

def run(tmp_filepath, history_filepath, typestr):	
	usr_df = read_userhis(history_filepath)
	user_mapping = create_index(usr_df['user_id'].unique())
	item_mapping = create_index(usr_df['item_id'].unique())

	print (typestr)
	print ('Writing at %s...' %tmp_filepath)
	if os.path.exists(tmp_filepath) == False:
		os.mkdir(tmp_filepath)
	count_df = pd.DataFrame({'item_cnt':[len(item_mapping)],'user_cnt':[len(user_mapping)]})
	count_df.to_csv('%s/count.csv' % tmp_filepath, index = False)

	if typestr != 'all':
		if 'main_cate' in usr_df.columns:
			cate_df = usr_df[usr_df['main_cate'] == typestr]
			if len(cate_df) > 0:
				usr_df = cate_df
			else:
				print ('%s does not exist' % typestr)
		else:
			print ('main_cate does not exist')
	if 'main_cate' not in usr_df.columns:
		usr_df['main_cate'] = [typestr] * len(usr_df)

	iteminfo_df = get_iteminfo(usr_df, None, item_mapping)
	item_filename = '%s/itemcnt.csv' % (tmp_filepath)
	print (item_filename)
	iteminfo_df[['item_id', 'item_idx', GRAPH_FEATURE, 'main_cate', 'play_cnt', 'user_cnt', 'count']].to_csv(item_filename, index = False)   

	usrcnt_df, usr_df_aslist = get_usrhis_byindex(usr_df, user_mapping, item_mapping)
	usercnt_filename = '%s/%s_usercnt.csv' % (tmp_filepath, typestr)
	print (usercnt_filename)
	usrcnt_df[['user_id', 'user_idx', 'count']].to_csv(usercnt_filename, index = False)
	usrhis_aslist_filename = '%s/%s_history_aslist.csv' % (tmp_filepath, typestr)
	print (usrhis_aslist_filename)
	usr_df_aslist[['user_idx', 'items']].to_csv(usrhis_aslist_filename, index = False)    


