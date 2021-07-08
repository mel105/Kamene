function [maxValPeakHist] = stablePeak(dataVec, k)
  % stablePeak odhadne najvyznamnejsi vrchol (peak) diferencovaneho histogramu. 
  % Diferencovane data  su dataVec data a uvazuje sa k-ta diferencia.
  
  arguments
    dataVec(:,1) double {mustBeNonempty};
    k(1,1) double {mustBeGreaterThanOrEqual(k,1)};
  end
  
  import Src.*;
  
  nVals = numel(dataVec);
  
  % k-diferencie
  nDiff = nVals-k;
  kDiff = NaN(1,nDiff);

  % vektor diferencii zohladnujuci k-ty krok
  for iDiff = 1:nDiff
    
    kDiff(iDiff) = dataVec(iDiff+k) - dataVec(iDiff);
  end
  
  % je to sirka binu. Otazka je, ako ju odvodit? Ja uvazujem jedno (vlastne dve) percento z medianu
  % spocitany zo vstupnych dat. Dve percenta preto, ze ako keby doprava a doleva od medianu.
  bandwidth = 2*0.01*median(dataVec); 
  
  [estPeakHist] = kDiffValHist(kDiff, bandwidth);

  % je to normovana hodnota, takze maxVal bude max 1;
  maxValPeakHist = max(estPeakHist) / nDiff;
end