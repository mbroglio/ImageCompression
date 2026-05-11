%% launch my DCT code in 2D (for simplicity we take N*N arrays)
clear all, close all, clc

param=0.2; % to be taken between 0 and 1

% f=@(x,y) 1;
% f=@(x,y) exp(.5*x.*y).*x.*(1-x).*y*(1-y);
f=@(x,y) sign(x-0.5).*sign(y-.5);
N=8;

f_mat=zeros(N);
for j=1:N
    for ell=1:N
        x_val=(2*j-1)/(2*N);
        y_val=(2*ell-1)/(2*N);
        f_mat(j,ell)=f(x_val,y_val);
    end
end

% f_mat=[231 32 233 161 24 71 140 245
% 247 40 248 245 124 204 36 107
% 234 202 245 167 9 217 239 173
% 193 190 100 167 43 180 8 70
% 11 24 210 177 81 243 8 112
% 97 195 203 47 125 114 165 181
% 193 70 174 167 41 30 127 245
% 87 149 57 192 65 129 178 228];

figure(1);
bar3(f_mat);
movegui('northwest');
title('Original bidemensional array f')


[c_mat]=dct_2D(f_mat);
movegui('southwest');
title('DCT of the original bidimensional f')

%% qua faccio sorta di JPG 2D
c_mat_reduced=c_mat;
c_mat_reduced(ceil(N*param)+1:end,ceil(N*param)+1:end)=0;
c_mat_reduced(1:ceil(N*param)+1,ceil(N*param)+1:end)=0;
c_mat_reduced(ceil(N*param)+1:end,1:ceil(N*param)+1)=0;

figure
bar3(c_mat_reduced);
movegui('northeast');
title('Truncated frequencies')

f_mat_reduced=idct_2D(c_mat_reduced);
movegui('southeast');
title('Bidimensional array corresponding to truncated frequencies')

% figure
% bar3(abs(f_mat-f_mat_reduced));
% title('absolute value of the error')