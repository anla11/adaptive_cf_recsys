/*	
	@author: anla
*/
	
#include <bits/stdc++.h>
#include "relative/relgraph_object.h"
#include "awc/awcgraph_object.h"

using namespace std;


/* ----------------- READ DEG of ITEMS ----------------- */
void 	read_count(string filename, int &n_users, int &n_items)
{
	ifstream file (filename.c_str()); // declare file stream: http://www.cplusplus.com/reference/iostream/ifstream/
	string token1, token2;
	bool skipheader = true;
	if (skipheader)
		getline(file, token1, '\n');
	getline (file, token1, ',' ); 
	getline (file, token2, '\n' );
	if (token1.size() > 0)
		n_items = atoi(token1.c_str());
	if (token2.size() > 0)
		n_users = atoi(token2.c_str());
	// cout << n_users << " " << n_items << endl;
}


/* ----------------- READ DEG of ITEMS ----------------- */
void 	read_itemdeg(string filename, int n_items, vector<int> &item_userdeg)
{
	ifstream file (filename.c_str()); // declare file stream: http://www.cplusplus.com/reference/iostream/ifstream/
	string id, cnt, tmpstr;
	bool skipheader = true;

	item_userdeg.resize(n_items);
	while (file.good())
	{	
		if (skipheader)
		{
			getline(file, id, '\n');
			skipheader = false;
			continue;
		}		
		getline (file, id, ',' ); 
		getline (file, id, ',' ); 
		getline (file, cnt, ',');
		getline (file, tmpstr, '\n');

		if (id.size() > 0)
		{
			
			int i = atoi(id.c_str()); 
			int v;
			v = atoi(cnt.c_str()); 
			item_userdeg[i] = v;
		}
	}
	file.close();
}

/* ----------------- READ DEG of ITEMS ----------------- */
void 	read_userdeg(string filename, int n_users, vector<int> &user_itemdeg)
{
	ifstream file (filename.c_str()); // declare file stream: http://www.cplusplus.com/reference/iostream/ifstream/
	string id, cnt;
	bool skipheader = true;

	user_itemdeg.resize(n_users);
	while (file.good())
	{
		if (skipheader)
		{
			getline(file, id, '\n');
			skipheader = false;
			continue;
		}		
		getline (file, id, ',' ); 
		getline (file, id, ',' ); 
		getline (file, cnt, '\n' );

		if (id.size() > 0)
		{
			int i = atoi(id.c_str()); 
			int v = atoi(cnt.c_str()); 
			user_itemdeg[i] = v;
			n_users = max(n_users, i);
		}
	}
	file.close();
}


/* ----------------- READ USER HISTORY ----------------- */
void 	read_usrhis(string filename, ItemGraph_Object &ig_ob, void (ItemGraph_Object::*func)(int, vector<int>&))
{
	ifstream file (filename.c_str()); // declare file stream: http://www.cplusplus.com/reference/iostream/ifstream/
	string user_id, listitem, token;
	bool skipheader = true;

	int cnt_user = 0;
	int cnt_zero = 0;
	int idx = 0;

	while (file.good())
	{
		if (skipheader)
		{
			getline(file, user_id, '\n');
			skipheader = false;
			continue;
		}	
		getline(file, user_id, ',');
		getline(file, token, '[');
		getline(file, listitem, ']');
		getline(file, token, '\n');
		if (listitem[listitem.size() -1] != ' ')
			listitem.push_back(' ');
		stringstream s(listitem);
		vector<int> items;
		items.resize(0);

		if ((user_id.size() > 0) && (listitem.size() > 0))
		{
			++cnt_user;
			int uid = atoi(user_id.c_str());
			while (getline(s, token, ' ')) 
			{
				if (token.size() > 0)
				{
					int item = atoi(token.c_str());
					items.push_back(item);
					if (ig_ob.item_userdeg[item] == 0)
						cnt_zero += 1;
				}
			}
			if (items.size() > 0)
				(ig_ob.*func)(uid, items);
		}
	}
	file.close();
}
