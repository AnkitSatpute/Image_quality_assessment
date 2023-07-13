from __future__ import absolute_import, division, print_function
import numpy as np
from utils import _initial_check,_get_sigmas,_get_sums,Filter,fspecial,filter2

def _vif_single(Org,Dis,sigma_n):
	"""
 	Add comment
 	"""
	EPS = 1e-10 #tolernace for zero variance. Variance below this is set to zero, 
	#and zero is set to this value to avoid numerical issues such as multiplication by zero in some cases
	num =0.0
	den =0.0
	for scale in range(1,5):
		#will go from 1,2,3,4
		# compute the size of the window used in the distortion channel estimation
		N=2.0**(4-scale+1)+1
		win = fspecial(Filter.GAUSSIAN,ws=N,sigma=N/5)
		if scale >1:
			Org = filter2(Org,win,'valid')[::2, ::2]
			Dis = filter2(Dis,win,'valid')[::2, ::2]
		
		#getting variances
		Org_sum_sq,Dis_sum_sq,Org_Dis_sum_mul = _get_sums(Org,Dis,win,mode='valid')
		#print(Org_sum_sq)
		#getting covariances
		sigmaOrg_sq,sigmaDis_sq,sigmaOrg_Dis = _get_sigmas(Org,Dis,win,mode='valid',sums=(Org_sum_sq,Dis_sum_sq,Org_Dis_sum_mul))
  		#get rid of numerical problems, very small negative numbers, or very
  		#small positive numbers, or other theoretical impossibilities.
		sigmaOrg_sq[sigmaOrg_sq<0]=0
		#print(sigmaGT_sq)
		sigmaDis_sq[sigmaDis_sq<0]=0
		#regression step to get values of g i.e.
		g=sigmaOrg_Dis /(sigmaOrg_sq+EPS)
		#Variance of error in regression
		sv_sq=sigmaDis_sq-g*sigmaOrg_Dis
		
		#get rid of numerical problems, very small negative numbers, or very
  		#small positive numbers, or other theoretical impossibilities.
		g[sigmaOrg_sq<EPS]=0
		sv_sq[sigmaOrg_sq<EPS]=sigmaDis_sq[sigmaOrg_sq<EPS]
		sigmaOrg_sq[sigmaOrg_sq<EPS]=0
		
		g[sigmaDis_sq<EPS]=0
		sv_sq[sigmaDis_sq<EPS]=0
		# constrain g to be non-negative.
		sv_sq[g<0]=sigmaDis_sq[g<0]
		g[g<0]=0
		#take care of numerical errors, vv could be very small negative
		sv_sq[sv_sq<=EPS]=EPS
		#print(np.sum([[1,2],[3,4]]))
	#denominator deontes reference image information (E)
	#numerator denotes distorted image information (F)
	# g= gi.......sigmaGT_sq= (Si^2 * Lamb(k))......sv_sq = sigma(v)^2.......sigma_n = sig(n)^2
		num += np.sum(np.log10(1.0+(g**2.)*sigmaOrg_sq/(sv_sq+sigma_n)))
		den += np.sum(np.log10(1.0+sigmaOrg_sq/sigma_n))
		#print(num/den)

	return num/den

def vif(Org,Dis,sigma_n=2):
	"""calculates Pixel Based Visual Information Fidelity (vif).

	Org: first (original) input image.
	Dis: second (deformed) input image.
	sigma_n: variance of the visual noise (default = 2)
	"""
	Org,Dis = _initial_check(Org,Dis)
	#checking whther we are getting correct index within 0 and 1 or not
	#print(Org.shape[2])
	"""print(Org[:,:,0])
	print(GT[:,:,1])
	print(GT[:,:,2])
	print(GT[:,:,3])
	"""
	#print(_vifp_single(GT[:,:,1],P[:,:,1],sigma_n))
	# GT,P = GT[:,:,np.newaxis],P[:,:,np.newaxis]
	#3 times because of r, g, b separate calculations
	return np.mean([_vif_single(Org[:,:,i],Dis[:,:,i],sigma_n) for i in range(Org.shape[2])])
