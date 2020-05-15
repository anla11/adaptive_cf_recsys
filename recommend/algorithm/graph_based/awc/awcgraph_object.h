/*	
	@author: anla
*/
	
#include <iostream>
#include "../itemgraph_object.h"

class AWC_Object: public ItemGraph_Object
{
public:
	AWC_Object()
	{
		n_users = n_items = 0;
		item_userdeg.resize(0);
		user_itemdeg.resize(0);
		for (int i = 0; i < MAX_ITEM; ++i)
			L[i].resize(0);
	}	

	float AWC_LAMBDA_CONST, AWC_GAMMA_CONST; 
	void 	update_parameters(float awc_lambda, float awc_gamma)
	{
		AWC_GAMMA_CONST = awc_gamma;
		AWC_LAMBDA_CONST = awc_lambda;
	}

	float  	cal_userweight(vector<int> & history)
	{
		float wj = 0;
		for (int r = 0, sz = history.size(); r < sz; ++r)
		{
			int item_rec = history[r];
		    float w_jalpha = cal_power(item_userdeg[item_rec], AWC_GAMMA_CONST);						
		    wj += w_jalpha;
		}
		return wj;
	}
	
	float   cal_itemrelation(int item_his, int item_rec)
	{
		int rec_deg = item_userdeg[item_rec];
		int his_deg = item_userdeg[item_his];
		return cal_power(his_deg, AWC_GAMMA_CONST - AWC_LAMBDA_CONST)*cal_power(rec_deg, AWC_LAMBDA_CONST - 1);
	}
};
