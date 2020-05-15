import pandas as pd
import numpy as np
import gc
from lib.userhistory_lib.numpyprocess_lib import binary_vector, binary_vector_fromlist, create_vector, stack_df, filteridx_matrix

def create_mapping_id2num(item_list):
	return dict(zip(item_list, range(len(item_list))))

def conv_tonum(id_list, mapping_id2num):
	return list(map(lambda x: mapping_id2num[x], id_list))

def create_mapping_num2id(num_list, id_list):
	return dict(zip(num_list,id_list))

def conv_toid(num_list, mapping_num2id):
	return list(map(lambda x: mapping_num2id[x], num_list))

def convert_useraslist_tomatrix(userhistory_aslist, n_items):
	x = userhistory_aslist.groupby(['user_idx']).apply(lambda r: binary_vector_fromlist(n_items, list(r['items']))).reset_index(name='items_onehot')
	user_idx = np.array(x['user_idx']).astype(int)
	user_arr = stack_df(x['items_onehot'], (len(x), n_items))
	return user_idx, user_arr

def convert_useraslist_toweightmatrix(userhistory_aslist, n_items):
	x = userhistory_aslist.groupby(['user_idx']).apply(lambda r: create_vector(n_items, list(r['items']), list(r['date_level']))).reset_index(name='items_onehot')
	user_idx = np.array(x['user_idx']).astype(int)
	user_arr = stack_df(x['items_onehot'], (len(x), n_items))
	return user_idx, user_arr
	
def convert_usertomatrix(userhistory, n_items):
	x = userhistory.groupby(['user_id']).apply(lambda r: binary_vector(n_items, list(r['item_idx']))).reset_index(name= 'items_onehot')
	user_idx = np.array(x['user_id']).astype(int)
	user_arr = stack_df(x['items_onehot'], (len(x), n_items))
	return user_idx, user_arr

def convert_itemtomatrix(item_df, n_items):
	y = item_df.groupby(['item_rec']).apply(lambda r: create_vector(n_items, list(r['item_his']), list(r['score']))).reset_index(name= 'items_onehot')
	item_idx = np.array(y['item_rec']).astype(int)
	item_arr = stack_df(y['items_onehot'], (len(y), n_items))
	return item_idx, item_arr

def convert_todf(rec_matrix, user_idx, item_idx, NTOP):
	x, y = filteridx_matrix(rec_matrix, NTOP)
	rec_df = pd.DataFrame({'user_idx':user_idx[x], 'item_idx':item_idx[y], 'score':rec_matrix[x, y]})
	return rec_df

def mapping_id(idx_list, mapping_dict):
	inv_map = {v: k for k, v in mapping_dict.items()}
	return conv_toid(idx_list, inv_map)

def create_index(all_id):
	return create_mapping_id2num(all_id)

def write_iteminfo(usr_df, viewcount_df, item_mapping, typestr, INDEX_FOLDER):
	itemcnt_df = usr_df.groupby(['item_id'])['user_id'].nunique().reset_index(name = 'count')
	if viewcount_df is not None:
		maincate_df = usr_df[['item_id', 'main_cate']].drop_duplicates()	
		itemcnt_df = itemcnt_df.merge(maincate_df, on = ['item_id'], how = 'left')	
		itemcnt_df = itemcnt_df.merge(viewcount_df, on = ['item_id'], how = 'left')
	itemcnt_df['play_cnt'] = np.array(itemcnt_df['play_cnt'].fillna(0)).astype(int)
	itemcnt_df['user_cnt'] = np.array(itemcnt_df['user_cnt'].fillna(0)).astype(int)

	itemcnt_df['item_idx'] = conv_tonum(itemcnt_df['item_id'], item_mapping)    
	item_filename = '%s/%s_itemcnt.csv' % (INDEX_FOLDER, typestr)
	itemcnt_df['deg'] = itemcnt_df['count']
	print (itemcnt_df[['item_id', 'item_idx', 'play_cnt', 'user_cnt', 'count', 'deg']].head())
	itemcnt_df[['item_id', 'item_idx', 'play_cnt', 'user_cnt', 'count', 'deg']].to_csv(item_filename, index = False)   


def convert_indexusrhis(usr_df, user_mapping, item_mapping):
	item_idx = conv_tonum(usr_df['item_id'], item_mapping)
	user_idx = conv_tonum(usr_df['user_id'], user_mapping)
	usr_df.loc[:, 'user_idx'] = user_idx
	usr_df.loc[:, 'item_idx'] = item_idx

	usr_df_aslist = usr_df.groupby(['user_id', 'user_idx'])['item_idx'].unique().reset_index(name = 'items')
	usrcnt_df = pd.DataFrame({'user_id':usr_df_aslist['user_id'], 'user_idx':usr_df_aslist['user_idx'],\
							  'count':list(usr_df_aslist.apply(lambda r: len(r['items']), axis = 1))})
	usrcnt_df = usrcnt_df.set_index(['user_id','user_idx']).reset_index()
	return usr_df_aslist, usrcnt_df

def write_indexusrhis(usr_df, viewcount_df, user_mapping, item_mapping, typestr, INDEX_FOLDER): 
	usr_df_aslist, usrcnt_df = convert_indexusrhis(usr_df, user_mapping, item_mapping)

	usercnt_filename = '%s/%s_usercnt.csv' % (INDEX_FOLDER, typestr)
	print (usercnt_filename)
	usrcnt_df[['user_id', 'user_idx', 'count']].to_csv(usercnt_filename, index = False)
	
	usrhis_aslist_filename = '%s/%s_history_aslist.csv' % (INDEX_FOLDER, typestr)
	print (usrhis_aslist_filename)
	usr_df_aslist['items'] = usr_df_aslist['items'].apply(lambda r: "["+" ".join(map(str,r.tolist()))+"]")
	usr_df_aslist[['user_idx', 'items']].to_csv(usrhis_aslist_filename, index = False)    