'''
	__author__: anlnt2
'''

import time
from numba import jit, cuda, float32
import numpy as np 

TPB = 16
blockdim = TPB, TPB


@cuda.jit
def my_multi2d(A, B, C):
	# tx, ty = cuda.threadIdx.x, cuda.threadIdx.y
	# bx, by = cuda.blockIdx.x, cuda.blockIdx.y
	# bwx, bwy = cuda.blockDim.x, cuda.blockDim.y

	M, N = A.shape
	N, K = B.shape

	# j = by * bwy + ty
	# i = bx * bwx + tx
	i, j = cuda.grid(2)
	if i >= M or j >= K: 
		return 
	res = 0
	for t in range(N):
		res += A[i, t] * B[t, j]
	C[i, j] = res

@cuda.jit
def my_multi2d_sharemem(A, B, C):
	tx = cuda.threadIdx.x
	ty = cuda.threadIdx.y

	M, N = A.shape
	N, K = B.shape

	i, j = cuda.grid(2)
	if i >= C.shape[0] and j >= C.shape[1]: 
		return 

	sA = cuda.shared.array(shape=(TPB, TPB), dtype=float32)
	sB = cuda.shared.array(shape=(TPB, TPB), dtype=float32)	

	res = 0.0
	for z in range((N - 1) / TPB + 1):
		if z * TPB + ty >= N:
			sA[tx, ty] = 0
		else:
			sA[tx, ty] = A[i, z * TPB + ty]

		if z * TPB + tx >= N:
			sB[tx, ty] = 0
		else:	
			sB[tx, ty] = B[z * TPB + tx, j]

		cuda.syncthreads()

		for t in range(TPB):
			res += sA[tx, t] * sB[t, ty]
		cuda.syncthreads()

	C[i, j] = res

def matmul_cuda(a, b):
	M, N = a.shape
	N, K = b.shape
	griddim = int((M - 1) / blockdim[0]) + 1, int((K - 1) / blockdim[1]) + 1
	res2 = np.zeros((M, K))
	start = time.time()
	d_a = cuda.to_device(a)
	d_b = cuda.to_device(b)
	# d_r = cuda.to_device(res2)
	my_multi2d_sharemem[griddim, blockdim](d_a, d_b, res2)
	# res2 = d_r.copy_to_host()
	print (time.time() - start)
	return res2