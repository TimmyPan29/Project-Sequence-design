clear ;close all ; clc
filename=sprintf("C:/Users/f1406/CZCS/Filseq40_20.txt");
filename1=sprintf("C:/Users/f1406/CZCS/Filseq40_19.txt");
filenamei=sprintf("C:/Users/f1406/CZCS/Goodseq40_20.txt");
filenamei1=sprintf("C:/Users/f1406/CZCS/Goodseq40_19.txt");
G0=int8(importdata(filename));
G1=int8(importdata(filename1));
GS0=int8(importdata(filenamei));
GS1=int8(importdata(filenamei1));
count=0
tic
for i=2:1:size(G0,1)
    for k=2:1:size(G1,1)
        B=int8(G0(i,2:end)+G1(k,2:end));
%     ABS_B=abs(B); fastest non-linear operation I　can find
        SABS_B=sum(abs(B),2);
        FS=find(SABS_B==0);
        if length(FS)>=1
            fprintf("Father seq index for zcp= %d\n",i)
            fprintf("Mother seq index for zcp= %d\n",k)
            count=count+length(FS);
            fprintf("累積解的數目= %d\n",count)
        else
            continue;
        end
    end
end
toc

run E1_GCP_sumACCF_constrction8.m