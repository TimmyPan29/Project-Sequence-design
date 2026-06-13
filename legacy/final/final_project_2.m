clear all;close all ;clc
l = input('lenght: ');
l = l;
tic
front_l = l/2;
back_l = l - front_l;
optimalz = l/2;
amount = 2.^l;
% front_amuont = 2.^frount_l;
% back_amount = 2.^back_l;
list_of_seq = zeros(amount,l);
seq = zeros(1,l);
for i = 2:1:amount
    seq(l) = seq(l)+1;
    position = l;
    while(seq(position)>1 & position>1)
        seq(position) = 0;
        position = position - 1;
        seq(position) = seq(position) + 1;
    end
    list_of_seq(i,:) = seq;
end
toc
tic

list_of_GCS = [];
for i = 1:1:amount
    seq_i = list_of_seq(i,:);
    ACF_i = aacf_c(seq_i);
    for j = i:1:amount
        seq_j = list_of_seq(j,:);
        ACF_j = aacf_c(seq_j);
        for m = j:1:amount
            seq_m = list_of_seq(m,:);
            ACF_m = aacf_c(seq_m);
            for n = m:1:amount
                seq_n = list_of_seq(n,:);
                ACF_n = aacf_c(seq_n);
                sum_of_ACF = ACF_i + ACF_j + ACF_m + ACF_n;
%                 sum(sum_of_ACF(2:end) == 0)
                if sum(sum_of_ACF(2:end) == 0) == l-1 
                    list_of_GCS(end+1, :) = [i, j, m, n];
                end
            end
        end
    end
end
toc
tic
list_of_CZCS = [];
for i = 1:1:size(list_of_GCS,1)
    a = list_of_GCS(i,1);
    b = list_of_GCS(i,2);
    c = list_of_GCS(i,3);
    d = list_of_GCS(i,4);
    seq_a = list_of_seq(a,:);
    seq_b = list_of_seq(b,:);
    seq_c = list_of_seq(c,:);
    seq_d = list_of_seq(d,:);
    CCF_ab = accf(seq_a,seq_b);
    CCF_bc = accf(seq_b,seq_c);
    CCF_cd = accf(seq_c,seq_d);
    CCF_da = accf(seq_d,seq_a);
    sum_of_CCF = CCF_ab + CCF_bc + CCF_cd +CCF_da;
    if sum(sum_of_CCF == 0) == l
        list_of_CZCS(end+1,:) = [seq_a, seq_b, seq_c, seq_d];
    end
end
list_of_CZCS(end,:)

toc

