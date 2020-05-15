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

from recommend.function.offline_cf.read_functions import read_his_fullinfo
from recommend.algorithm.cf.postprocess_useritem_awc import recommend, read_itemmatrix

from lib.utils.indexprocess_lib import create_index, convert_indexusrhis
from lib.utils.scoredate_lib import decay_bydate, get_datescore, sub_date
from configuration.algorithm_config.cf_algconfig import DATE_LEVEL_HYBRID, REDUCE_CYCLE

def run(outputpath, tmppath, hispath, typestr):
	print ('Read history: ')
	start = time.time()
	usr_df, all_item = read_his_fullinfo(outputpath, tmppath, hispath, typestr)
	user_mapping = create_index(usr_df['user_id'].unique())
	item_mapping = create_index(all_item['item_id'].unique())

	now = datetime.datetime.now()
	usr_df['int_date'] = 0
	usr_df = usr_df.sort_values(by = 'user_id')
	itemweight_aslist = usr_df.groupby(['user_id']).apply(lambda r: decay_bydate(get_datescore(list(r['int_date']), DATE_LEVEL_HYBRID), REDUCE_CYCLE)).reset_index(name = 'date_level')
	usrhis_aslist, _ = convert_indexusrhis(usr_df, user_mapping, item_mapping)
	usrhis_aslist = usrhis_aslist.merge(itemweight_aslist, on = ['user_id'])

	del usr_df
	del all_item
	gc.collect()
	print (time.time() - start)

	usergroup = "wide"
	itemmatrix_filename = '%s/%s_itemmatrix_%s.csv' % (outputpath, typestr, usergroup)
	output_path = '%s/%s_awc_useritem_%s' % (outputpath, typestr, usergroup)

	print (itemmatrix_filename)
	start = time.time()
	itemmatrix_df = read_itemmatrix(itemmatrix_filename, item_mapping)
	print (time.time() - start)

	recommend(usrhis_aslist, itemmatrix_df, (user_mapping, item_mapping), output_path)
	del itemmatrix_df
	gc.collect()
