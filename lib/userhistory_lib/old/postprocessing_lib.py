import pandas as pd
import numpy as np
import time
import re

def read_file(typestr):
    data = np.loadtxt('matrix/matrix_%s.txt' % typestr)
    item_df = pd.DataFrame({'item_1':np.array(data[:, 0]).astype(int), 'item_2': np.array(data[:, 1]).astype(int), 'score':data[:, 2]})
    item_cnt = pd.read_csv('data/itemcnt_%s.csv' % typestr, dtype = str)
    item_cnt['item_idx'] = np.array(item_cnt['item_idx']).astype(int)
    item_cnt['count'] = np.array(item_cnt['count']).astype(int)
    item_df = item_df.merge(item_cnt, how = 'left', left_on = ['item_1'], right_on = ['item_idx'])
    del item_df['item_idx']
    item_df.rename(columns = {'item_id':'item1_id', 'count': 'item1_cnt'}, inplace = True)
    item_df = item_df.merge(item_cnt, how = 'left', left_on = ['item_2'], right_on = ['item_idx'])
    del item_df['item_idx']
    item_df.rename(columns = {'item_id':'item2_id', 'count': 'item2_cnt'}, inplace = True)
    item_df = item_df.sort_values(by = 'item1_id', ascending = [1])
    usercnt = pd.read_csv('data/usercnt_%s.csv' % typestr, dtype = str)
    usercnt['count'] = np.array(usercnt['count']).astype(int)
    usercnt['user_idx'] = np.array(usercnt['user_idx']).astype(int)

    usrhis_aslist = pd.read_csv('data/history_%s.csv' % typestr, dtype = str)
    usrhis_aslist['user_idx'] = np.array(usrhis_aslist['user_idx']).astype(int)
    cov_items = usrhis_aslist['items'].apply(lambda r: str2int(r[1:-1]))    
    usrhis_aslist.drop(columns = ['items'])
    usrhis_aslist['items'] = cov_items    
    return item_df, usrhis_aslist, item_cnt, usercnt
    
def str2int(string):
    string = re.sub(' +',' ',string)
    tmp = re.split(' ', string.strip())
    return np.array(tmp).astype(int)    

def create_mapping_num2id(num_list, id_list):
    return dict(zip(num_list,id_list))

def conv_toid(num_list, mapping_num2id):
    return list(map(lambda x: mapping_num2id[x], num_list))

def binary_vector(sz, num):
    a = np.zeros(sz).astype(int)
    a[np.array(num[0])] = 1
    return a

def create_vector(sz, num, values):
    a = np.zeros(sz).astype(float)
    a[np.array(num)] = values
    return a

def unpivot(frame):
    N, K = frame.shape
    data = {'score' : frame.values.ravel('F'),
            'item_2' : np.asarray(frame.columns).repeat(N),
            'user_idx' : np.tile(np.asarray(frame.index), K)}
    return pd.DataFrame(data, columns=['user_idx', 'item_2', 'score'])

def stack_df(data, arr_size, sz):
    arr = np.empty(arr_size)
    n_container = int((len(data) - 1)/sz+1)
    for i in range(n_container):
        from_idx, to_idx = i * sz, min((i+1)*sz, len(data))
        arr[from_idx:to_idx] = np.vstack(data.iloc[from_idx: to_idx])
    return arr

def convert_usertomatrix(userhistory_aslist, n_items, sz = 10000):
    x = userhistory_aslist.groupby(['user_idx']).apply(lambda r: binary_vector(n_items, list(r['items']))).reset_index(name= 'items_onehot')
    user_idx = x['user_idx']
    user_arr = stack_df(x['items_onehot'], (len(x), n_items), sz)
    return user_idx, user_arr

def convert_itemtomatrix(item_df, n_items, sz = 10000):
    y = item_df.groupby(['item_2']).apply(lambda r: create_vector(n_items, list(r['item_1']), list(r['score']))).reset_index(name= 'items_onehot')
    item_idx = y['item_2']
    item_arr = stack_df(y['items_onehot'], (len(y), n_items), sz)
    return item_idx, item_arr

def recommend_bymatrix(userhistory_aslist, item_df):
    n_items = max(item_df['item_1'])+1
    user_idx, user_arr = convert_usertomatrix(userhistory_aslist, n_items)
    item_idx, item_arr = convert_itemtomatrix(item_df, n_items)
    return pd.DataFrame(np.dot(user_arr, item_arr.T), columns = item_idx), user_idx, item_idx

def recommend_bydf(userhistory_aslist, item_df):
    rec_df, user_idx, item_idx = recommend_bymatrix(userhistory_aslist, item_df)
    rec_df['user_idx'] = user_idx
    rec_df['item_2'] = item_idx
    rec_df = unpivot(rec_df[(list(['user_idx']) + list(item_idx))].set_index(['user_idx']))
    rec_df = rec_df.sort_values(by = ['user_idx','score'], ascending = [1, 0])
    return rec_df

def mapping_id(rec_df, item_cnt, user_cnt):
    item_cnt = item_cnt.sort_values(by = ['item_idx'], ascending = [1])
    item_mapping = create_mapping_num2id(item_cnt['item_idx'], item_cnt['item_id'])
    item_id = conv_toid(rec_df['item_2'], item_mapping)
    user_cnt = user_cnt.sort_values(by = ['user_idx'], ascending = [1])
    user_mapping = create_mapping_num2id(user_cnt['user_idx'], user_cnt['user_id'])
    user_id = conv_toid(rec_df['user_idx'], user_mapping)
    rec_df['item_id'] = item_id
    rec_df['user_id'] = user_id
    rec_df.drop(columns = ['user_idx', 'item_2'], inplace = True)
    return rec_df[['user_id', 'item_id', 'score']]