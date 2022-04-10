function [res, f] = sequentialHistogram(dataVec)
  % Algoritmus je zalozeny na tejto myslienke: Existuje nieco ako sekvencny, diferencny histogram,
  % to znamena, ze spocitas diference z dat v dataVec a z diferencii vyrobis histogram a odhadnes si
  % jeho maximalny peak (bin, v ktorom je najviac dat). Tuto diferenciu urobis s krokom 1, to
  % znamena, ze diferencujes dva susedne vzorky v dataVec. To iste urobis pre krok 2, t.j.
  % diferencujes obvzorky a odhadnes max. peak. A takto pokracujes az do nejakeho max kroku (uplne
  % najviac max krok zrejme bude n-1, kde n je rozmer dataVec). No a pokial je dataVec periodicky s
  % jednou dominantnou periodou, tak tato perioda v t sekvencnom histograme bude opakovat a to prave
  % v zavislosti na tom, aka velka je ta perioda. Takze si vysledujeme priebeh max peakov a pokial v
  % rozumnych intervaloch budeme vidiet tie periody, tak to znamena, ze mame signal s dominantnou
  % jednou periodou. Ak nie, tak potom nastane ten druhy pripad.
  %
  % Vyhody: metoda ma logicky a aj matematicky vyznam - i ked neviem, ako by som to matematicky 
  % opisal. Ale videl som par clankov, kde to pouzivali, alebo podobny postup.
  % Nevyhody: No zase je to zavisle na nastaveni par veci. A) ako nastavit prah priepustnosti, B)
  % ako signal vyhladit, ak ho potrebujem vyhladzovat. C) Ak ho vyhladzovat nepotrebujem, ako
  % efektivne z maxPeaksVec odhadnut najvyznamnejsie hodnoty?
  
  arguments
    dataVec (:,1) double {mustBeNonempty};
  end
  
  import Src.*;
  
  kMax = ceil(numel(dataVec)*0.8); %povedzme, ze budeme diferencovat max. do 80% rozmeru signalu.
  
  % 
  kVec = NaN(kMax-1,1);
  maxPeaksVec = NaN(kMax-1, 1);

  for k = 1:1:kMax

    maxPeaksVec(k) = Src.stablePeak(dataVec, k);
    kVec(k) = k;
  end

  % aj tu maxPeaksVec potrebujeme vyhladit.
  bw = 1000*bandwidth(maxPeaksVec);
  [maxPeaksVecSmt] = kernelSmoother(maxPeaksVec, bw);
  
  % najdem  body zvratu vo vyhladenej rade
  [~, uppPeaks] = turningPoints(maxPeaksVecSmt);
  [idxUpp, ~, uppVals] = find(uppPeaks);
  
  % odhadneme si prah priepustnosti, t.j. nejaku hranicu, ktora mi vyznaci tie vyznamnejsie body
  % zvratu. Pre tento ucel treba pouzijeme medzikvartilove rozpatie IQR..
  q = quantile(maxPeaksVec, [0.25 0.75]); 
  q = 1.5*diff(q);
  
  % najdeme si body zvratu (idxPos) vacsie ako prah priepustnosti (q)
  idx = uppVals >= q;
  idxPos = idxUpp(idx);
  
  % odvodenie ficury f. Myslienka je ta z uvodu popisu, teda vychadza z principu sekv.
  % histogramu.Podla neho, periodicky signal sa v sekvencom histograme prejavi tak, ze po nejakej
  % periode sa opakujem.
  % Ak je nas signal teda periodicky s jednou dominantnou periodou, potom sa mi staci pozriet na dva
  % vyznamnejsie peaky hore vyhladeneho vektora a rozdiel tychto dvoch peakov by mal odpovedat cirka
  % indexu prveho z nich. Ak to tak nie je, tak v periodickom signale je viacej vyznamnejsich
  % frekvencii.
  
  if ~isempty(idxPos) && numel(idxPos) >= 2
    
    f = (idxPos(2) - idxPos(1)) / idxPos(1);
    
    if f >= 0.75
      res = "categoryA";
    else
      res = "categoryB";
    end
    
  else
    
    res = nan;
    f = nan;
  end
  
  % kreslitko
  figure('Name', 'MaximalneNormovanePeakyDiffHistogramu')  
  plot(kVec, maxPeaksVec, '-')
  hold on
  plot(kVec, maxPeaksVecSmt, '-')
  hold on
  yline(q, '-g')
  hold on
  plot(idxPos, maxPeaksVecSmt(idxPos), 'o', 'MarkerEdgeColor', 'm', 'MarkerFaceColor', 'g')
  legend("maximalne normovane peaky v sekvencnom histograme pre krok - k", ...
    "vyhladeny priebeh maximalnych normovanych peakov", ...
    "prah priepustnosti", "Vyznamne peaky")
  xlabel("k")
end