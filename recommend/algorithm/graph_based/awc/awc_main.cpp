#include <bits/stdc++.h>
#include "../functions.h"
#include "../../../../configuration/algorithm_config/cf_algconfig.h"
/*
	@author: anla
*/

using namespace std;

string preprocess_folder, output_folder, typestr, lambda_str, gamma_str;

int main(int argc, char *argv[])
{
	if (argc > 5)
	{
		cout << "Wrong command!\n";
		return 0;
	}	
	preprocess_folder = argv[1];
	output_folder = preprocess_folder;
	typestr = argv[2];

	string count_filename     = preprocess_folder + "/count.csv";
	string itemdeg_filename   = preprocess_folder + "/itemcnt.csv";
	string userdeg_filename   = preprocess_folder + "/" + typestr+ "_usercnt.csv";
	string history_filename   = preprocess_folder + "/" + typestr+ "_history_aslist.csv";

	int external_param_flat = 0;
	float awc_lambda, awc_gamma;
	AWC_Object awc;
	vector<string> groups;

	if (argc == 5)
	{
		lambda_str = argv[3];
		gamma_str = argv[4];
		awc_lambda = atof(lambda_str.c_str());
		awc_gamma = atof(gamma_str.c_str());  
		awc.update_parameters(awc_lambda, awc_gamma);
		external_param_flat = 1;
		cout << "External lambda gamma: " << awc_lambda << " "<< awc_gamma <<"\n";
	}	
	
	cout << "User groups: ";
	get_usergroup(typestr, groups);
	for (int i = 0; i < int(groups.size()); i++)
		cout << groups[i] << " ";
	cout << "\n";

	cout << "Reading files" << "\n";			
	cout << "\t" << count_filename << "\n";
	read_count(count_filename, awc.n_users, awc.n_items);
	cout << "\t" << itemdeg_filename << "\n";
	read_itemdeg(itemdeg_filename, awc.n_items, awc.item_userdeg);
	cout << "\t" << userdeg_filename << "\n"; 
	read_userdeg(userdeg_filename, awc.n_users, awc.user_itemdeg);  

	cout << "Write matrix\n";
	// do not print anything else when starting this loop
	for (int i = 0; i < int(groups.size()); i++)
	{
		string group = groups[i];

		if (external_param_flat == 0)
		{
			get_parameters(typestr, awc_lambda, awc_gamma, group);
			awc.update_parameters(awc_lambda, awc_gamma);
		}
		//init
		string MODE = "CAL_MATRIX";
		if (MODE == "CAL_MATRIX")
		{
			read_usrhis(history_filename, awc, &AWC_Object::cal_itemmatrix);
			awc.addedge_kstepneighbors(k_neighbor_step);
			string matrix_filename = output_folder + "/" + typestr + "_matrix_" + group + ".txt";
			awc.write_matrix(matrix_filename);
		}
	}
	
	return 0;
}
