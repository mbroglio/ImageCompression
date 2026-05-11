%% INPUT: c_vect original Fourier coefficients
%%        N number of intervals
%% AIM  : plot Fourier coefficients and IDCT with bars

function [f_vect]=idct_1D(c_vect)

N=length(c_vect);

[D]=compute_D(N);
f_vect=D'*c_vect;

figure;
bar(f_vect);


return