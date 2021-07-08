function [qData] = quantile(data, p)
  % funkcicka spocita p-kvantil. Poznamka, p = 0.5 = median (snad to takto vychadza. Treba kontrola)
  
  arguments
    data (:,1) double {mustBeNonempty};
    p (:,:) double {mustBePositive, mustBeInRange(p, 0, 1)};
  end
  
  dataLen = size(data, 1);
  dataSort = sort(data, 1);
    
  idx = (2 * dataLen * p + 1) / 2;
  idx(idx <= 1) =  1;
  idx(idx >= dataLen) = dataLen;
  idxF = floor(idx);
    
  dataSort(end+1, :) = 1;
  qData = dataSort(idxF,:) + (dataSort(idxF+1,:) - dataSort(idxF,:)).* (idx - idxF).';
end
