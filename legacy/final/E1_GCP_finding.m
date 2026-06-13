clear ; close all ; clc
L = input('length: ');
different_sign = input('different_sign: ');
prefix = input('prefix at least 1 : ');

k=different_sign;
count=0;
temp1=ceil(L/2)-1;
A1=zeros(1,different_sign);
SaveGoodSeq=zeros(1,L);
SaveiSeq=zeros(1,1);
SaveFilseq=zeros(1,L);
% main function
total = nchoosek(L-prefix, k);
if isinf(total) % Can overflow, give useful error for that case.
    error(message('MATLAB:pmaxsize'));
end
% P = zeros(total, k,"int8");

% Compute P one row at a time:
tic
ind = 1:k;
V=int8(1:L-prefix);
n=length(V);
P=zeros(1,k,"int8");
for w=2:ceil(total)
    % Find right-most index to increase
    % j = find(ind < n-k+1:n, 1, 'last');
    for j = k:-1:1 
        if ind(j)<n-k+j 
            break; 
        end
    end
    
    % Increase index j, initialize all indices to j's right.
    % ind(j:k) = (ind(j) + 1) : (ind(j) + 1 + k - j);
    % P(i, :) = v(ind);
    for t=1:j-1
        P(1, t) = V(ind(t));
    end
    indj = ind(j) - j + 1;
    for t = j:k 
        ind(t) = indj + t;
        P(1, t) = V(indj + t);
    end
    A1=P+prefix;
    Fdseq=finding_seqL(double(A1),L);
    Filseq=aacf_c(Fdseq);
    if length(find(Filseq==0))==temp1
        SaveGoodSeq(end+1,:)=Fdseq;
        SaveiSeq(end+1,:)=w;
        SaveFilseq(end+1,:)=Filseq;
    end
end

% mkdir C:/Users/f1406 CZCS
filename=sprintf("C:/Users/f1406/CZCS/Goodseq32_15.txt");
filename1=sprintf("C:/Users/f1406/CZCS/iSeq32_15.txt");
filename2=sprintf("C:/Users/f1406/CZCS/Filseq32_15.txt");
tic
save(filename,'SaveGoodSeq','-ascii')
save(filename1,"SaveiSeq",'-ascii','-double')
save(filename2,"SaveFilseq",'-ascii')

toc
