function [bw] = bandwidth(data)
  % Funkcia odhadne sirku vyhladzovacieho okna. 
  
  residuaVec = abs(data - median(data));
  medianResidual = median(residuaVec);
  
  
  sigma_H = medianResidual / 0.6745;
  
  bw = sigma_H * (4.0 / (3.0 * numel(data)) )^0.2;
end