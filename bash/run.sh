datadir="movielen"
outputpath="$datadir/output"
trainpath="$datadir/input/movielen_train.csv"
testpath="$datadir/input/movielen_test.csv"
tmppath="$datadir/tmp"
typestr="None"

# GPU run
# export NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
# export NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice
# export NUMBAPRO_CUDA_DRIVER=/usr/local/cuda/lib64/libcudart.so

g++ -o recommend/algorithm/graph_based/awc/awc_main recommend/algorithm/graph_based/awc/awc_main.cpp
python3 recommend/function/offline_cf/main.py --mode preprocess --outputpath $outputpath --tmppath $tmppath --train $trainpath --type $typestr

for param_gamma in "-1.0" "-0.5" "0.5" "0.0" "-0.25" "0.25" 
do
	for param_lambda in "0.2" "0.3" "0.5" "0.7" "1.0"
	do
		param_str="$param_lambda,$param_gamma"

		new_outputpath="$outputpath/$para"

		echo $train_date $test_date $hour $CF_TMP_DIR $para

		mkdir $new_outputpath
		resdir="$outputpath/*"

		python3 recommend/function/offline_cf/main.py --mode itemmatrix --outputpath $outputpath --tmppath $tmppath --type $typestr
		python3 recommend/function/offline_cf/main.py --mode recommend --outputpath $outputpath  --tmppath $tmppath --train $trainpath --test $testpath --type $typestr
		mv $resdir $new_outputpath
		python3 recommend/function/offline_cf/main.py --mode evaluate --outputpath $new_outputpath  --tmppath $tmppath --train $trainpath --test $testpath --type $typestr --param $param_str
		python3 recommend/function/offline_cf/main.py --mode test --outputpath $new_outputpath  --tmppath $tmppath --train $trainpath --test $testpath --type $typestr --param $param_str
	done
done