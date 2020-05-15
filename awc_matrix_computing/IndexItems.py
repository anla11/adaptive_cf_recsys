import numpy as np
from lib.utiles.numpyprocess_lib import filteridx_matrix

class IndexItems():
	def __init__(self, ItemIDs):
		self.ItemIDs = ItemIDs

	def get_itemidx(self, items):
		find_items = lambda x: np.where(np.array(self.ItemIDs)==x)[0][0]
		idx_items = np.apply_along_axis(find_items, 1, np.array(items).reshape(-1, 1))        
		return idx_items

	def gettoprec_byid(self, idx_start_items, rec_matrix, metric, NTOP=5):
		items, rec_items = filteridx_matrix(rec_matrix, NTOP, metric=metric)
		return pd.DataFrame({'his_id':np.array(self.ItemIDs)[idx_start_items[items]], \
							 'rec_id':np.array(self.ItemIDs)[rec_items], \
							 'score':rec_matrix[items, rec_items]})        
