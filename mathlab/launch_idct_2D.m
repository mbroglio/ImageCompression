%% launch my IDCT code in 1D
clear all, close all, clc

N=10;
% c_mat=zeros(N); c_mat(end-1,end-1)=1;
c_mat=zeros(N); c_mat(ceil(N/2),ceil(N/2))=1;
% c_mat=zeros(N); c_mat(2,2)=1;
% c_mat=zeros(N); c_mat(1,1)=1;

figure(1);
bar3(c_mat);

f_mat=idct_2D(c_mat);