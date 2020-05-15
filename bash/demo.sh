datadir="movielen"
outputpath="$datadir/output"
trainpath="$datadir/input/movielen_train.csv"
testpath="$datadir/input/movielen_test.csv"
tmppath="$datadir/tmp"
typestr="None"
param_lambda=0.3
param_gamma=-5.0

# GPU run
# export NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
# export NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice
# export NUMBAPRO_CUDA_DRIVER=/usr/local/cuda/lib64/libcudart.so

param_str="$param_lambda,$param_gamma"
python3 recommend/function/offline_cf/main.py --mode preprocess --outputpath $outputpath --tmppath $tmppath --train $trainpath --type $typestr

g++ -o recommend/algorithm/graph_based/awc/awc_main recommend/algorithm/graph_based/awc/awc_main.cpp
./recommend/algorithm/graph_based/awc/awc_main $tmppath $typestr $param_lambda $param_gamma
python3 recommend/function/offline_cf/main.py --mode itemmatrix --outputpath $outputpath --tmppath $tmppath --type $typestr
python3 recommend/function/offline_cf/main.py --mode recommend --outputpath $outputpath  --tmppath $tmppath --train $trainpath --test $testpath --type $typestr
python3 recommend/function/offline_cf/main.py --mode evaluate --outputpath $outputpath  --tmppath $tmppath --train $trainpath --test $testpath --type $typestr --param $param_str
python3 recommend/function/offline_cf/main.py --mode test --outputpath $outputpath  --tmppath $tmppath --train $trainpath --test $testpath --type $typestr --param $param_str