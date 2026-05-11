%% INPUT: c_mat original Fourier coefficients
%%        N number of intervals (for simplicity we take square matrices)
%% AIM  : plot Fourier coefficients and IDCT with bars

function [f_mat]=idct_2D(c_mat)

N=size(c_mat,1);

[D]=compute_D(N);

f_mat=c_mat;

%% Faccio IDCT1 per colonne
for j=1:N
    f_mat(:,j)=D'*f_mat(:,j);
end

%% Faccio IDCT1 per righe
for j=1:N
    f_mat(j,:)=(D'*f_mat(j,:)')';
end

figure;
bar3(f_mat);

return