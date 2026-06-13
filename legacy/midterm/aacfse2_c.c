#include <math.h>
#include "mex.h"

#define	MAT1 prhs[0]	
#define	OUT  plhs[0]	

void mexFunction(
	int nlhs,	mxArray *plhs[],
	int nrhs, const mxArray *prhs[]) 
{
	double	*out, *mat1;
	int m, p,i, j, count, temp;

	if (nrhs!=1)
		mexErrMsgTxt("PAIRDIST requires one input arguments.");
	
	p  = mxGetM(MAT1);
	m  = mxGetN(MAT1);

	if (p != 1)
		mexErrMsgTxt("Matrix sizes mismatch!");
	
	if (!mxIsNumeric(MAT1) || mxIsSparse(MAT1)  || !mxIsDouble(MAT1))
		mexErrMsgTxt("Input 1 is not a full numerical array!");

	OUT = mxCreateDoubleMatrix(p,(m-1)/2,mxREAL);

	out = mxGetPr(OUT);
	mat1 = mxGetPr(MAT1);
	temp=(m+1)/2;
	for (i=1; i<temp; i++){
		count=0;
		for (j=0; j<m-i; j++){
			if(mat1[i+j]==mat1[j]){
				count+=1;
			}	
		}
		out[i-1]=-m+i+count+count;
	}			
	
}