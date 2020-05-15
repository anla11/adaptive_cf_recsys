import numpy as np 
import pandas as pd 
from log_parser import LOG_PARSER
from AWC import AWC_REC

datapath ='input/log.csv'
log_df = pd.read_csv(datapath)

log_parser = LOG_PARSER(log_df)
awc = AWC_REC(log_parser, parameters={'gamma':0.5, 'lambda':0.7})
item_his = log_parser.get_itemids()[0]
rec_df = awc.recommend(item_his)
print (rec_df)