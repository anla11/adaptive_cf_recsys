/*	
	@author: anla
*/
	
#include <bits/stdc++.h>
#include "../functions.h"

using namespace std;

string preprocess_folder, output_folder, typestr;

int main(int argc, char *argv[])
{
	if (argc != 3)
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
	string matrix_filename    = output_folder + "/" + typestr+ "_matrix.txt";

	RELSET_Object relative_set;

	cout << count_filename << "\n";
	read_count(count_filename, relative_set.n_users, relative_set.n_items);
	cout << itemdeg_filename << "\n";
	read_itemdeg(itemdeg_filename, relative_set.n_items, relative_set.item_userdeg);
	cout << userdeg_filename << "\n"; 
	read_userdeg(userdeg_filename, relative_set.n_users, relative_set.user_itemdeg);  

	read_usrhis(history_filename, relative_set, &RELSET_Object::cal_itemmatrix);
	cout << "Write matrix at: " << matrix_filename<< "\n";
	relative_set.write_matrix(matrix_filename);	
	return 0;
}