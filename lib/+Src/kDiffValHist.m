function [h] = kDiffValHist(dataVec, binwidth)
  % funkcia obsahuje alg. na odhad diff. histogramu
  %
  
  nData = length(dataVec);
  sortData = sort(dataVec);

  % inic. pomocnych poli
  h = zeros(1,nData);
  binEdgesLow = zeros(1,nData);
  binEdgesHigh = zeros(1,nData);

  binEdgesLow(1) = sortData(1);
  binEdgesHigh(1) = binwidth + binEdgesLow(1);

  h(1) = 1;
  iBin = 1;

  for iPri = 2:nData
  
    if (sortData(iPri) <= binEdgesHigh(iBin))
      
      h(iBin) = h(iBin) +1;
    else
      
      iBin = iBin +1;
      binEdgesLow(iBin) = sortData(iPri);
      binEdgesHigh(iBin) = binwidth + binEdgesLow(iBin);
      h(iBin) = h(iBin) +1;
    end
  end

  h((iBin+1):end) = [];
end