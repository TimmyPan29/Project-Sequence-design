#include <math.h>
#include "mex.h"

#define	MAT1 prhs[0]	
#define	OUT  plhs[0]	

void mexFunction(
	int nlhs,	mxArray *plhs[],
	int nrhs, const mxArray *prhs[]) 
{
	double	*out, *mat1;
	int m, p, j, A, i;

	if (nrhs!=1)
		mexErrMsgTxt("PAIRDIST requires one input arguments.");
	
	p  = mxGetM(MAT1);
	m  = mxGetN(MAT1);

	if (p != 1)
		mexErrMsgTxt("Matrix sizes mismatch!");
	
	if (!mxIsNumeric(MAT1) || mxIsSparse(MAT1)  || !mxIsDouble(MAT1))
		mexErrMsgTxt("Input 1 is not a full numerical array!");

	OUT = mxCreateDoubleMatrix(p,37,mxREAL);

	out = mxGetPr(OUT);
	mat1 = mxGetPr(MAT1);
	
	
	for (j=0; j<m; j++){
		A=mat1[j]-1;
		if(j%2==0)
		{
			for(i=A; i<37 ; i++){
				out[i]=1;
			}
		}
		else
		{
			for(i=A; i<37 ; i++){
				out[i]=0;
			}
		}
	}
}