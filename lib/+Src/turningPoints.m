function [lowPeaksVec, uppPeaksVec] = turningPoints(dataVec)
  % funkcia spocita body zvratu
  
  nData = numel(dataVec);
  
  lowPeaksVec = zeros(nData,1);
  uppPeaksVec = zeros(nData,1);
    
  for it = 2:nData-1
    
    if (dataVec(it-1) >= dataVec(it)) && (dataVec(it) < dataVec(it+1))
      
      lowPeaksVec(it) = dataVec(it);
    end
    
    if (dataVec(it-1) <= dataVec(it)) && (dataVec(it) > dataVec(it+1))
      
      uppPeaksVec(it) = dataVec(it);
    end
  end
  
end