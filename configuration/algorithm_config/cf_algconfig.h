#include <iostream>

int k_neighbor_step = 1;

void 	get_usergroup(string typestr, vector<string> &groups)
{
	groups.resize(0);
	groups.push_back("wide");
}

void 	get_parameters(string typestr, float &AWC_LAMBDA, float &AWC_GAMMA, string usergroup)
{
	AWC_LAMBDA = 0.3;
	AWC_GAMMA = -0.25;
	if (typestr == "all")
	{
		if (usergroup == "wide")
		{
			AWC_LAMBDA = 0.3;
			AWC_GAMMA = -0.5;
		}
		if (usergroup == "pop")
		{
			AWC_LAMBDA = 0.5;
			AWC_GAMMA = 0.0;
		}
		if (usergroup == "unpop")
		{
			AWC_LAMBDA = 0.3;
			AWC_GAMMA = -0.5;
		}
	}
}
