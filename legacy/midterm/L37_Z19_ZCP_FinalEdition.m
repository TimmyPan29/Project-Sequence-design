clear ; close all ;clc
l = input('length: ');
left_different_sign = int8(input('left_different_sign: '));
prefix = input('prefix at least 1 : ');
tic
n= l - prefix;
n = int8(1:1:n);
df_p = nchoosek1(n,left_different_sign);
df_p = df_p + int8(prefix/2);
size(df_p,1)
toc
tic
Si=zeros(1,1,'double');
SFseq=zeros(1,(l+1)/2-1,'int8');
seq = zeros(size(df_p,1),l,"logical");
for i = 1:1:size(df_p,1) % ith sequence
    seq(i,:)=finding_seq37(double(df_p(i,:)));
    B=aacfse2_c(double(seq(i,:)));
    if length(find(B==0))==9
%         SFseq=cat(1,SFseq,B);
%         Si=cat(1,Si,i);
        SFseq(end+1,:)=B;
        Si(end+1,:)=double(i);
    else
        continue;
    end    
end
size(SFseq)

toc
filename=sprintf("F:/ZCP/aacfse2Seq37.txt");
filename1=sprintf("F:/ZCP/Si_37.txt");
tic
save(filename,"SFseq",'-ascii',"-int8")
save(filename1,"Si",'-ascii','-double')
toc

% run("V2_FindZCP.m")
function c = nchoosek1(v,k)
%NCHOOSEK Binomial coefficient or all combinations.
%   NCHOOSEK(N,K) where N and K are non-negative integers returns N!/K!(N-K)!.
%   This is the number of combinations of N things taken K at a time.
%   When a coefficient is large, a warning will be produced indicating
%   possible inexact results. In such cases, the result is only accurate
%   to 15 digits for double-precision inputs, or 8 digits for single-precision
%   inputs.
%
%   NCHOOSEK(V,K) where V is a vector of length N, produces a matrix
%   with N!/K!(N-K)! rows and K columns. Each row of the result has K of
%   the elements in the vector V. This syntax is only practical for
%   situations where N is less than about 15.
%
%   Class support for inputs N,K:
%      float: double, single
%      integer: uint8, int8, uint16, int16, uint32, int32, uint64, int64
%
%   Class support for inputs V:
%      float: double, single
%      integer: uint8, int8, uint16, int16, uint32, int32, uint64, int64
%      logical, char
%
%   See also PERMS.

%   Copyright 1984-2018 The MathWorks, Inc.

if ~isscalar(k) || k < 0 || ~isreal(k) || k ~= round(k)
    error(message('MATLAB:nchoosek:InvalidArg2'));
end

if ~isvector(v)
    error(message('MATLAB:nchoosek:InvalidArg1'));
end

% the first argument is a scalar integer
if isscalar(v) && isnumeric(v) && isreal(v) && v==round(v) && v >= 0
    % if the first argument is a scalar, then, we only return the number of
    % combinations. Not the actual combinations.
    % We use the Pascal triangle method. No overflow involved. c will be
    % the biggest number computed in the entire routine.
    %
    n = v;  % rename v to be n. the algorithm is more readable this way.
    if isinteger(n)
        if ~(strcmp(class(n),class(k)) || isa(k,'double'))
            error(message('MATLAB:nchoosek:mixedIntegerTypes'))
        end
        classOut = class(n);
        inttype = true;
        int64type = isa(n,'int64') || isa(n,'uint64');
    elseif isinteger(k)
        if ~isa(n,'double')
            error(message('MATLAB:nchoosek:mixedIntegerTypes'))
        end
        classOut = class(k);
        inttype = true;
        int64type = isa(k,'int64') || isa(k,'uint64');
    else % floating point types
        classOut = superiorfloat(n,k);
        inttype = false;
        int64type = false;
    end
    
    if k > n
        error(message('MATLAB:nchoosek:KOutOfRange'));
    elseif ~int64type && n > flintmax
        error(message('MATLAB:nchoosek:NOutOfRange'));
    end
    
    if k > n/2   % use smaller k if available
        k = n-k;
    end
    
    if k <= 1
        c = n^k;
    else
        if int64type
            % For 64-bit integers, use an algorithm that avoids
            % converting to doubles
            c = binCoef(n,k,classOut);
        else
            % Do the computation in doubles.
            nd = double(n);
            kd = double(k);
            
            nums = (nd-kd+1):nd;
            dens = 1:kd;
            nums = nums./dens;
            c = round(prod(nums));
            
            if ~inttype && c > flintmax(classOut)
                warning(message('MATLAB:nchoosek:LargeCoefficient', ...
                    sprintf( '%e', flintmax(classOut) ), floor(log10(flintmax(classOut)))));
            end
            % Convert answer back to the correct type
            c = cast(c,classOut);
        end
    end
    
else
    % the first argument is a vector, generate actual combinations.
    
    k = double(k);
    n = length(v);
    if iscolumn(v)
        v = v.';
    end
    
    if n == k
        c = v;
    elseif n == k + 1
        c = repmat(v,n,1);
        c(1:n+1:n*n) = [];
        c = reshape(c,n,k);
    elseif k == 1
        c = v.';
    elseif k == 0
        c = reshape(v([]), 1, 0);
    elseif k > n
        c = reshape(v([]), 0, k);
    else
        if isnumeric(v) && ~isobject(v)
           c = combs(v,k);
        else
           c = combs(1:n,k);
           c = v(c);
        end
    end

end


function c = binCoef(n,k,classOut)
% For integers, compute N!/((N-K)! K!) using prime factor cancellations

numerator = cast((n-k+1):n,classOut);
for denominator = k:-1:1
    F = factor(denominator);
    for whichfactor = 1:numel(F)
        thefactor = F(whichfactor);
        largestMultiple = find(mod(numerator,thefactor) == 0, 1, 'last');
        numerator(largestMultiple) = numerator(largestMultiple)/thefactor;
    end
end
c = prod(numerator,'native');
end


function P = combs(v,k)
%COMBS  All possible combinations.
%   COMBS(1:N,M) or COMBS(V,M) where V is a row vector of length N,
%   creates a matrix with N!/((N-M)! M!) rows and M columns containing
%   all possible combinations of N elements taken M at a time.
%
%   This function is only practical for situations where M is less
%   than about 15.

v = v(:).'; % Make sure v is a row vector.
n = length(v);

total = uint32(nchoosek(n, k)/10);
if isinf(total) % Can overflow, give useful error for that case.
    error(message('MATLAB:pmaxsize'));
end
P = zeros(total, k,"int8");

% Compute P one row at a time:
ind = 1:k;
P(1, :) = v(1:k);%只影響第一行
for i=2:total %開始影響第二列
    % Find right-most index to increase
    % j = find(ind < n-k+1:n, 1, 'last');
    for j = k:-1:1 
        if ind(j)<n-k+j %n永遠6 k永遠3
            break; %跳出去這圈for 到下面statement
        end
    end
    
    % Increase index j, initialize all indices to j's right.
    % ind(j:k) = (ind(j) + 1) : (ind(j) + 1 + k - j);
    % P(i, :) = v(ind);
    for t=1:j-1
        P(i, t) = v(ind(t));
    end
    indj = ind(j) - j + 1;
    for t = j:k %j=3:k=3
        ind(t) = indj + t;
        P(i, t) = v(indj + t); %第二列第三行填4 v向量是1x18 從1~18
    end
end
end
end