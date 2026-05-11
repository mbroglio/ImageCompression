%% Compute DCT matrix
%% INPUT:  N size of the vector to transform
%% OUTPUT: matrix D representing the DCT transformation

function [D]=compute_D(N)

alpha_vect=zeros(N,1);
alpha_vect(1)=N^(-.5); alpha_vect(2:end)=N^(-.5)*sqrt(2);

for k=1:N
    for i=1:N
        D(k,i)=alpha_vect(k)*cos((k-1)*pi*(2*i-1)/(2*N));
    end
end

return