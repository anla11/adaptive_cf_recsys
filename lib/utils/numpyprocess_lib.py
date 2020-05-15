'''
    __author__: anlnt2
'''

import numpy as np
import gc 

def binary_vector(sz, num):
    a = np.zeros(sz).astype(int)
    a[np.array(num)] = 1
    return a

def binary_vector_fromlist(sz, num):
    a = np.zeros(sz).astype(int)
    a[np.array(num[0])] = 1
    return a

def create_vector(sz, num, values):
    a = np.zeros(sz).astype(float)
    a[np.array(num)] = values
    return a

def stack_df(data, arr_size, container_size = 100000):
    arr = np.empty(arr_size).astype(float)
    n_container = int((len(data) - 1)/container_size+1)
    for i in range(n_container):
        from_idx, to_idx = i * container_size, min((i+1)*container_size, len(data))
        arr[from_idx:to_idx] = np.vstack(data.iloc[from_idx: to_idx])
        gc.collect()        
    return arr

def gettopidx_row(x, NTOP):
    res = np.argsort(x)[:NTOP]
    return res

def gettopidx_eachrow_matrix(arr, NTOP):
    return np.apply_along_axis(gettopidx_row, 1, -arr, NTOP)

def keeppositive_idx(arr):
    x, y = np.where(arr > 0)
    return x, y

def filteridx_matrix(arr, NTOP):
    '''
        - Sorted and limit NTOP idx of each row
        - Remove <= 0 idx of each row
        - Return idx of arr
    '''
    top_idx = gettopidx_eachrow_matrix(arr, NTOP)
    top_value = np.array([arr[i, top_idx[i]] for i in range(len(top_idx))])
    x, y = keeppositive_idx(top_value)
    return x, top_idx[x, y]
