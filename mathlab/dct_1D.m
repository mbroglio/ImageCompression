%% INPUT: f_vect array
%%        N number of intervals
%% AIM  : plot standard function and DCT with bars

function [c_vect]=dct_1D(f_vect)

N=length(f_vect);
[D]=compute_D(N);
c_vect=D*f_vect;

figure;
bar(c_vect);

return