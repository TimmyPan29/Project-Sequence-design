%% interleaving reshape([[M1:M2],1,[]])
ipt0=input("enter a first GCP index  : ");
ipt1=input("enter a second GCP index  : ");
S0=GS0(ipt0,:);
S1=GS1(ipt1,:);
S2=flip(S1);
S3=bitxor(flip(S0),1);
C0=reshape([S0;S2],1,[]);
C1=reshape([S1;S3],1,[]);
C2=bitxor(C0,1);
C3=C1;

AACF0=aacf_c(double(C0));
AACF1=aacf_c(double(C1));
AACF2=aacf_c(double(C2));
AACF3=aacf_c(double(C3));

ACCF0=accf_c(double(C0),double(C1));
ACCF1=accf_c(double(C1),double(C2));
ACCF2=accf_c(double(C2),double(C3));
ACCF3=accf_c(double(C3),double(C0));

sumAACF=AACF0+AACF1+AACF2+AACF3; %T1 property
sumACCF=ACCF0+ACCF1+ACCF2+ACCF3; %T2 property


