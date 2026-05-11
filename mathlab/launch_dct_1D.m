%% launch my DCT code in 1D
clear all, close all, clc

% parametro ``compressione'' da fissare tra 0 e 1
param=0.1;

% f=@(x) 1;
% f=@(x)exp(3*x).*x.*(1-x);
f=@(x) sign(x-0.5);
N=100;

f_vect=zeros(N,1);
for j=1:N
    x_val=(2*j-1)/(2*N);
    f_vect(j)=f(x_val);
end
% f_vect=2*(rand(N,1)-.5);
figure(1);
bar(f_vect);
movegui('northwest');
title('Original vector f')

[c_vect]=dct_1D(f_vect);
movegui('southwest');
title('DCT of the original vector f')


%% qua faccio sorta di JPG 1D
c_vect_reduced=c_vect;
c_vect_reduced(ceil(N*param)+1:end)=0;
figure
bar(c_vect_reduced);
movegui('northeast');
title('Truncated frequencies')


f_vect_reduced=idct_1D(c_vect_reduced);
movegui('southeast');
title('Vector corresponding to truncated frequencies')
