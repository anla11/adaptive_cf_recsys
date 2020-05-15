import numpy as np
from IndexItems import IndexItems
from log_parser import LOG_PARSER

class AWC_REC(IndexItems):
	def __init__(self, log_parser, parameters={'gamma':0.5, 'lambda':0.7}):
		IndexItems.__init__(self, log_parser.get_itemids())
		self.log_parser = log_parser
		self.HisMatrix = log_parser.get_hismatrix()
		self.k_item = np.array(log_parser.get_itemcnt()).reshape((-1))
		self.gamma, self.lam = parameters['gamma'], parameters['lambda']
		self.ItemMatrix, self.RecMatrix = None, None

	def __get_itemuser_matrix(self):
		T = self.HisMatrix * (self.k_item ** self.gamma)
		#normalize
		sumrow_T = np.sum(T, axis=1) 
		T_trans = T.T
		T = (T_trans * (1/sumrow_T)).T
		return T

	def __get_weight_matrix(self):
		k_item_inv = 1/self.k_item
		H = np.dot(k_item_inv.reshape(-1, 1)**self.lam, k_item_inv.reshape(1,-1)**(1-self.lam))
		return H

	def get_itemitem_matrix(self):
		if self.ItemMatrix is None:
			T = self.__get_itemuser_matrix()
			H = self.__get_weight_matrix()
			self.ItemMatrix = H * np.dot(self.HisMatrix.T, self.HisMatrix*T)
			np.nan_to_num(self.ItemMatrix, copy=False)
		return self.ItemMatrix

	def __recommend_itemidx(self, start_idx):
		tmp_W = self.get_itemitem_matrix()[:, start_idx].T
		return tmp_W

	def recommend(self, start_items, NTOP=5):
		idx_start_items = self.get_itemidx(start_items)
		score_metric = self.__recommend_itemidx(idx_start_items)
		return self.gettoprec_byid(idx_start_items, score_metric, metric='sim', NTOP=NTOP)

	def __get_useridx(self, id_users):
		find_users = lambda x: np.where(np.array(self.log_parser.get_userids())==x)[0][0]
		idx_users = np.apply_along_axis(find_users, 1, np.array(id_users).reshape(-1, 1))        
		return idx_users

	def get_useritem_matrix(self):
		W = self.get_itemitem_matrix()
		return np.dot(self.HisMatrix, W.T)      

	def recommend_byusers(self, user_id, NTOP=5):
		user_idx = self.__get_useridx(user_id)
		user_his_idx = np.where(self.HisMatrix[user_idx]==1)[1]
		score_metric = self.__recommend_itemidx(user_his_idx)
		rec_df = self.gettoprec_byid(user_his_idx, score_metric, metric='sim')
		return rec_df.groupby(['rec_id'])['score'].sum().reset_index(name='score').sort_values(by='score', ascending=0).head(NTOP)