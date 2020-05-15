import pandas as pd 
import numpy as np
from lib.utils.indexprocess_lib import create_mapping, convert_mapping

class LOG_PARSER():
	def __init__(self, log_df, user_df=None, items_df=None, user_key='user_id', item_key='item_id'):
		'''
			log_df: log data as pandas dataframe
				|user_id|item_id|...
			user_df: information of all users
			items_df: information of all items
		'''
		self.log_df = log_df
		self.user_key, self.item_key = user_id, item_id
		self.data_packages, self.his_matrix = None, None

		self.user_df = None
		if user_df is None:
			self.user_df = log_df[user_id].value_counts().reset_index(name='user_cnt').rename(columns={'index':user_key})
		else:
			self.user_df = user_df

		self.item_df = None
		if item_df is None:
			self.item_df = log_df[item_id].value_counts().reset_index(name='item_cnt').rename(columns={'index':item_key})
		else:
			self.item_df = item_df

	def parse(self):
		if self.data_packages != None:
			return self.data_packages

		his_df = self.log_df[[self.user_key, self.item_key]].dropna().drop_duplicates()
		user_mapping = create_mapping(his_df[self.user_key].unique(), range(len(self.user_df)))
		item_mapping =create_mapping(self.items_df[self.item_key], range(len(self.items_df)))
	
		his_df['user_idx'] = convert_mapping(user_mapping, his_df[self.user_key])
		his_df['item_idx'] = convert_mapping(item_mapping, his_df[self.item_key])

		Sizes = {'Log':len(his_df), 'Users':len(self.user_df), 'Items':len(self.items_df)}
		self.data_packages = Sizes, his_df, self.user_df, self.items_df
		return self.data_packages

	def get_hismatrix(self):
		if self.his_matrix != None:
			return self.his_matrix
		Sizes, his_df, _, _ = self.parse()
		self.his_matrix = np.zeros((Sizes['Users'], Sizes['Items']))
		self.his_matrix[np.array(self.his_df['user_idx']), np.array(self.his_df['item_idx'])]=1
		return self.his_matrix

	def get_userids(self):
		return self.user_df[self.user_key]

	def get_itemids(self):
		return self.user_df[self.item_key]

	def get_itemcnt(self):
		return self.item_df['item_cnt']		