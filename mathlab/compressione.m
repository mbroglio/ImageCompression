%% esempio di codice di compressione e decompressione blocco 8*8
clear all, close all, clc

%% costruzione matrice di quantizzazione
q = 60; % quality (prenderlo tra 1 e 100)
if q > 50
     qf = (100-q)/50;
else    
     qf = 50/q; 
end
Q = qf*[16 11 10 16 24 40 51 61 ;
        12 12 14 19 26 58 60 55 ;
        14 13 16 24 40 57 69 56 ;
        14 17 22 29 51 87 80 62 ;
        18 22 37 56 68 109 103 77 ;
        24 35 55 64 81 104 113 92 ; 
        49 64 78 87 103 121 120 101 ;
        72 92 95 98 112 100 103 99];
Q = round(Q); 
Q = max(1,Q); % copre il caso q=100 (cosi viene Q di tutti uni)
disp('Matrice di quantizzazione')
Q
pause

%% Costruisco una matrice 8*8 ``farlocca'' che rappresenta scala di grigi
A = zeros(8);
for i=1:8
    for j=1:8
%         A(i,j) = (i-1)^2*(j)*(8-j);
%          A(i,j) = floor(rand(1,1)*256);
    end
end
A=[52 55 61 66 70 61 64 73;  63 59 55 90 109 85 69 72;  62 59 68 113 144 104 66 73;  63 58 71 122 154 106 70 69;  67 61 68 104 126 88 68 70 ; 79 65 60 70 77 68 58 75;  85 71 64 59 55 61 65 83;  87 79 69 68 65 76 78 94];
disp('matrice iniziale 8x8')
A
% A = round(255*A/max(max(A)))
% A = uint8(A); 
pause

%% COMPRESSIONE
disp('tolgo 128')
AA2 = A-128*ones(8)
pause

disp('Opero la DCT2')
AA2 = dct_2D(AA2)
pause

disp('Divido per la quantization-matrix e arrotondo al intero')
AA2 = round(AA2./Q)  % immagine compressa
pause

% DECOMPRESSIONE
disp('ri-moltiplico per Q')
A2 = AA2.*Q
pause

disp('opero la Inverse DCT2')
A2 = idct_2D(A2)
pause

disp('ri-aggiungo 128, arrotondo al intero e impongo [0,255]')
A2 = round(A2 + 128*ones(8));
A2 = max(0,min(A2,255))    % questo serve a tagliarlo in [0,255]
pause

% A2 = uint8(A2);
disp('confronto con la A originale')
A