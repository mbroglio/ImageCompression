%% launch my IDCT code in 1D
clear all, close all, clc

N=100;
% c_vect=zeros(N,1); c_vect(end-1)=1;
% c_vect=zeros(N,1); c_vect(ceil(N/2))=1;
c_vect=zeros(N,1); c_vect(2)=1;

figure;
bar(c_vect);

f_vect=idct_1D(c_vect);