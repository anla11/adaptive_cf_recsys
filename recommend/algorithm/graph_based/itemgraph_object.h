/*	
	@author: anla
*/

#ifndef ITEMGRAPH_OBJECT_H
#define ITEMGRAPH_OBJECT_H

#include <iostream>
#include <math.h>     
#include "constant.h"

using namespace std;
typedef pair<int , float> pif;
struct compare{
	inline bool operator()(const pif &a, const pif &b) 
	{   
		return (a.second != b.second ? a.second > b.second : a.first == b.first);
	}   
} ;

float cal_power(float a, float b)
{
	float tmp = pow(a, abs(b));
	if (b < 0)
		return 1/tmp;
	else
		return tmp;			
}

float cal_2stepedge(float a, float b)
{
	// adjust function here
	return min(a, b)/2;
}


class ItemGraph_Object
{
public:
	int n_users; //number of users
	int n_items; //number of items
	int n_edges; //number of edges in user-item graph

	vector<int> item_userdeg; //degree of item nodes in user-item graph
	vector<int> user_itemdeg; //degree of user nodes in user-item graph
	// user-item graph is not stored because of small memory size
	vector<pif> L[MAX_ITEM]; //item-item matrix, contains score of edges of item-item graph
		//L[alhpa][i] = (beta, score) means item alpha is recommended by item beta with score
	vector<int> item_itemdeg; //degree of item node in item-item graph

	ItemGraph_Object()
	{
		n_users = n_items = 0;
		item_userdeg.resize(0);
		user_itemdeg.resize(0);
		for (int i = 0; i < MAX_ITEM; ++i)
			L[i].resize(0);
		item_itemdeg.resize(0);
	}
	

	virtual float  	cal_userweight(vector<int> & history){
		return int(history.size());
	}

	virtual float   cal_itemrelation(int item_his, int item_rec)	{
		return 1;
	}

	virtual float 	cal_edgeweight(float userweight, int item_his, int item_rec)	{
		return (1/userweight) * cal_itemrelation(item_his, item_rec);
	}	

	virtual void 	cal_itemmatrix(int user_j, vector<int> &history)
	// history: list of idx of items selected by user_j
	{
		if (history.size() <= 1)
			return;
		float userweight = cal_userweight(history);

		for (int r = 0, sz = history.size(); r < sz; ++r)
		{
			int item_alpha = history[r];
			for (int q = 0; q < sz; ++q)
				if (r != q)
				{
					int item_beta = history[q];

					//get index of item_beta on L[item_alpha]
					int flag = -1;
					for (int k = 0, sz_alpha = L[item_alpha].size(); k < sz_alpha; ++k)
						if (L[item_alpha][k].first == item_beta)
						{
							flag = k;
							break;
						}

					if (flag == -1) 
					//if item_beta does not appear on L[item_alpha], 
					//		add item_beta to the end of list L[item_alpha] with zero-score
					{
						L[item_alpha].push_back(make_pair(item_beta, 0));
						flag = L[item_alpha].size()-1;
					}

					//flag now contains index of item_beta on the list L[item_alpha]
					float tmp = cal_edgeweight(userweight, item_beta, item_alpha);
					L[item_alpha][flag].second += tmp;
				}
		}
	}	

	virtual void 	write_matrix(string matrix_filename)
	{
		if (freopen(matrix_filename.c_str(), "w", stdout))
		{
			for (int i = 0; i < n_items; ++i)
				for (int t = 0, szi = L[i].size(); t < szi; ++t)
					if (L[i][t].second > 0)
						cout << i << " " << L[i][t].first << " " << L[i][t].second << "\n";
						// item_rec item_his score
			fclose (stdout);
		}
	}


	virtual void 	read_matrix(string matrix_filename, int inverse = 0)
	{
		ifstream iFile(matrix_filename.c_str());
	    while (!iFile.eof())
	    {
			int u, v;
			float t;
			iFile >> u >> v >> t;
			if (t > 0)
				if (inverse)
					L[v].push_back(make_pair(u, t));
					// read inverse of L
				else
					L[u].push_back(make_pair(v, t));
	    }
	}	

	virtual void 	recommend(vector<int> &his, vector<pif> &rec)
	// rec must have size of n_items
	{
		if (rec.size() < n_items)
			return;
		for (int t = 0; t < n_items; ++t)
			rec[t] = make_pair(t, 0);

		for (int q = 0, sz = his.size(); q < sz; ++q)
		{
			int item_beta = his[q];
			for (int t = 0, sz_beta = L[item_beta].size(); t < sz_beta; ++t)
			{
				int item_alpha = L[item_beta][t].first;
				float score = (rec[item_alpha].second + L[item_beta][t].second/n_users) ;
				rec[item_alpha] = make_pair(item_alpha, score);
			}
		}
	}

	virtual void 	addedge_kstepneighbors(int levels)
	{
		item_itemdeg.resize(n_items);
		while (levels--)
		{
			float mean = 0;
			for (int i = 0; i < n_items; ++i)
			{
				item_itemdeg[i] = int(L[i].size()); // save graph of k-1 previous levels
				mean += item_itemdeg[i] / n_items;
			}
			float approx_median = mean * approx_median_ratio;

			for (int item_1 = 0; item_1 < n_items; ++item_1)
			{
				// apply for unpopular items only
				if (item_itemdeg[item_1] > approx_median)
					continue;

				// find 2-step-neighbors for each node
				// note that just visit edges on graph of previous levels only, which is stored in item_itemdeg
				for (int q = 0, sz_1 = item_itemdeg[item_1]; q < sz_1; ++q)
				{
					int item_2 = L[item_1][q].first;
					int score_12 = L[item_1][q].second;

					for (int r = 0, sz_2 = item_itemdeg[item_2]; r < sz_2; ++r)
					{
						int item_3 = L[item_2][r].first;
						int score_23 = L[item_2][r].second;
						int j = -1;
						for (int t = 0, sz_1_new = L[item_1].size(); t < sz_1_new; ++t)
							if (L[item_1][t].first == item_3)
							{
								j = t;
								break;
							}

						if (j >= sz_1)
						// means item_3 appears on graph of current level.
						{
							int score = max(L[item_1][j].second, cal_2stepedge(score_12, score_23));
							// get max of old score and new score
							L[item_1][j] = make_pair(item_3, score);
							// replace score to current index of item_3, not create a new index 
						}
						else if (j == -1)
						// means (item_1, item_3) not in edge set ~ new connection for item_1
						{	
							int score = cal_2stepedge(score_12, score_23);
							L[item_1].push_back(make_pair(item_3, score));
							// add item_3 at the end of list neighbors of item_1 without changeing sz_1
						}
					}
				}
			}
		}
	}


};
#endif 
