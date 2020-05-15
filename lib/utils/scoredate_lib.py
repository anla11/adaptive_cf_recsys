'''
	__author__: anlnt2
'''

import datetime
import time
import pandas as pd
import numpy as np

def read_time(time_str):
	if pd.isnull(time_str):
		return None
	if time_str == '':
		return None
	return time.strptime(time_str, '%Y-%m-%d')

def sub_date(a, b):
	if pd.isnull(b):
		b = ''
	if pd.isnull(a):
		a = b
	ta = read_time(a)
	tb = read_time(b)

	if tb is None:
		tb = 0
	else:
		tb = (tb.tm_year -  2003) * 365 + tb.tm_yday
	
	if ta is None:
		return 0
	else:
		return (ta.tm_year -  2003) * 365 + ta.tm_yday - tb
	

def get_datelevel(intdate_arr):
	vmin, vmax = np.min(intdate_arr), np.max(intdate_arr)
	n = len(intdate_arr)
	if vmin == vmax:
		return np.zeros(n)
	step = int((vmax - vmin-1)/n+1)
	get_level = lambda x: int((x-vmin)/step)

	level = list(map(get_level, intdate_arr))
	return level

def get_dategroup(intdate_arr):
	level = get_datelevel(intdate_arr)
	level_unique = np.sort(np.unique(level))
	
	get_group = lambda x: np.where(level_unique == x)[0][0]
	group = list(map(get_group, level))
	return group

def get_datescore(intdate_arr, alpha = 0.3):
	vmin, vmax = np.min(intdate_arr), np.max(intdate_arr)
	level = get_datelevel(intdate_arr)
	return list(np.array((intdate_arr)-vmin)*alpha + np.array(level)*(1-alpha))

def decay_bydate(x, reduce_cycle = 0.5):
	return list(np.exp(-1 * np.log(1/(1-reduce_cycle))/1 * np.array(x)))
