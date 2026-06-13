clear ; close all ; clc

%Using Kronecker Product to let (14,12)-ZCP and (26,26)-ZCP form a
%(14*26,12*26)-ZCP = (364,312)-ZCP

%Use the ZCPs in Kernels
a=[1 1];
b=[1 -1];
c=[-1 -1 -1 -1 1 -1 -1 1 -1 -1 1 -1 -1 -1 1 1 1 1];
d=[-1 1 1 1 -1 -1 -1 1 -1 1 -1 1 1 -1 1 1 1 -1];
count=0;
%Some computation in Construction iii in handout
t1=(a+b)/2;
t2=(a-b)/2;
t3=(fliplr(a)-fliplr(b))/2; %fliplr(a) = reverse(a)
t4=(fliplr(a)+fliplr(b))/2;

F1=kron(c,t1)+kron(d,t2);
F2=kron(c,t3)-kron(d,t4);

tempF1XCOR=xcorr(F1);
tempF2XCOR=xcorr(F2);
F1XCOR=tempF1XCOR(1,364:length(tempF1XCOR));
F2XCOR=tempF2XCOR(1,364:length(tempF2XCOR));
tempZCP=F1XCOR+F2XCOR;
tempZCP(abs(tempZCP)<0.1)=0;
ZCP=tempZCP
for i=2:1:length(ZCP);
    if ZCP(1,i)==0
    count=count+1; 
    else
        break;
    end
end

%PAPR and PAV function
temp1=F2;
temp2=0;
t=linspace(0,1,1000);
for k=1:1:length(F1)
    temp2=temp2+(temp1(1,k))*exp(j*2*pi*k*t);
end
IAPR=temp2.*conj(temp2); %IAPR
plot(t,IAPR),title("IAPR(t)")
Pav=round(sum(1/length(t)*IAPR,2)); %Pav
PAPR=max(IAPR)/Pav;

fprintf("zone = Z = %d\n",count+1)
fprintf("PAPR = %2.3f",PAPR)

