'''
    __author__: anlnt2
'''

import numpy as np
import pandas as pd
from lib.utils.indexprocess_lib import convert_usertomatrix

def convert_totopmatrix(rec_df, item_cnt, NTOP_EVA):
    '''
        input:
            rec_df: .csv file, result of recommend algorithm
            'user_id|user_idx|item_id|score'
                user_id, item_id: string
                score: float

            item_cnt: .csv file, index and count on history of items
            'item_id|item_idx|count'
                item_id: string
                item_idx, count: int
        output:
            numpy 2d-array:
                if user i has recommended item alpha: rec_matrix[i,alpha] = 1, else = 0
    '''
    n_items = max(item_cnt['item_idx']) + 1
    rec_df['score'] = np.array(rec_df['score']).astype(float)
    rec_df = rec_df.sort_values(by = ['user_idx', 'score'], ascending = [1, 0])
    rec_ntop = rec_df.groupby(['user_idx']).apply(lambda r: \
            pd.DataFrame({'item_id':list(r['item_id'].iloc[:NTOP_EVA]), 'score':list(r['score'].iloc[:NTOP_EVA])})).reset_index().drop(columns = ['level_1'])
    rec_ntop = rec_ntop.merge(item_cnt[['item_id', 'item_idx', 'count']], on = ['item_id'], how = 'left')
    user_idx, rec_matrix = convert_usertomatrix(rec_ntop, n_items)
    return rec_matrix

def mean_row(arr):
    return np.mean(arr[arr > 0])

def cal_user_novelty(rec_matrix, item_cnt_arr):
    novel_matrix = rec_matrix * item_cnt_arr
    return np.apply_along_axis(mean_row, 1, novel_matrix)
    
def cal_novelty(novel_user):
    return np.mean(novel_user[np.isnan(novel_user) == False])

def cal_item_reccnt(rec_matrix, n_users, item_reccnt):
    n_item = rec_matrix.shape[1]
    item_reccnt_cur = np.sum(rec_matrix, axis = 0)
    item_reccnt += item_reccnt_cur
    return item_reccnt
    
def cal_coverage(item_reccnt):
    return np.mean(np.array(item_reccnt > 0))

def cal_diversity(reccnt, n_users, NTOP_EVA):
    inverse_reccnt = (n_users - reccnt)
    return np.sum(reccnt * inverse_reccnt) * 1/ (n_users**2 - n_users) / NTOP_EVA  
    
def cal_congestion(item_reccnt):
    reccnt_sorted = np.sort(item_reccnt)
    s = np.cumsum(reccnt_sorted)
    vmax = s[-1]
    s/=vmax
    n = len(s)
    return 1-2/n * np.sum(s[:-1])-1/n    