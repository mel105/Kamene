% skrip, ktory sa venuje kategorizaci periodickych signalov. Su k dispozicii zrejme dva typy
% signalov: 1) s pravidelnou periodou (dominantna zrejme jedna frekvencia) - CategoryA a 2) v signale 
% je viacej vyznamnych period - CategoryB. Uloha je kategorizovat, o aky typ signalu sa jedna.

import Src.*;

dataA = load(fullfile('Data', 'PR1')); dataA = mean(dataA.PR1);
dataB = load(fullfile('Data', 'PR1_2.mat')); dataB = mean(dataB.PR1);

% lokalne maxima
[f1] = localMaximaProcess(dataA)

% sekvencny histogram
[f2] = sequentialHistogram(dataA)

