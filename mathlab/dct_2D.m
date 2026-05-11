%% INPUT: f_mat double array
%%        N number of intervals (for simplicity we take square matrices)
%% AIM  : plot standard function and DCT with bars

function [c_mat]=dct_2D(f_mat)

N=size(f_mat,1);

[D]=compute_D(N);

c_mat=f_mat;
%% Faccio DCT1 per colonne
for j=1:N
    c_mat(:,j)=D*c_mat(:,j);
end

%% Faccio DCT1 per righe
for j=1:N
    c_mat(j,:)=(D*c_mat(j,:)')';
end

figure;
bar3(c_mat);

return