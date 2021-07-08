function [res, f] = localMaximaProcess(dataVec)
  % Postup je zalozeny na myslienke, ze si najdem lokalne maxima v signale. Z rozdielu indexov
  % maximalnych peakov zistim ich rozostup. Z rozostupu si spocitam ficuru/charakteristiku na
  % zaklade ktorej sa rozhodnem, ze ci sa jedna o signal s dominantnou periodou alebo nejedna.
  
  % Vyhody: Hlavne primitivny algoritmus
  % Nevyhody: Je potreba dataVec este vyhladit. Nachadzaju sa tan pidi lokalne maxima, ktore
  % nechecme. Pouzije sa zrejme vyhladzovacia metoda, ale ta pravdepodobne bude tiez zavisla na
  % nastaveni - napriklad sirka vyhldzovacieho okna - a to je ta hlavna nevyhoda, teda ak nastavit
  % to referencne okno?
  
  arguments
    dataVec (:,1) double {mustBeNonempty};
  end
  
  % kniznica, kde mam ulozene funkcie
  import Src.*;
  
  % pretoze sa vo vektore vyskytnu body zvratu, ktore nechcem, tak dataVec este vyhladim
  bw = bandwidth(dataVec)*100; % ako zvolit sirku vyhladzovacieho okna?
  [dataVec] = kernelSmoother(dataVec, bw);
  
  % tu najdeem lokalne maxima a minima, to znamena, ze nieco ako body zvratu.
  [~, uppPeaksVec] = turningPoints(dataVec);
    
  [idxUpp] = find(uppPeaksVec);
  
  % kreslitko
  figure('Name', 'Lokalne maxima')
  plot (dataVec)
  hold on
  plot(idxUpp, dataVec(idxUpp), 'ro')
  xlabel("IDX")
  ylabel("PR signal")
  legend("Anal signal", "odhad lokalnych maxim")
  
  % charakteristika je zalozena na tom, ze z rozdielov poloh lokalnych maxim si spocitam min a max
  % rozdielov. A nasledne si spocitam ich pomer, t.j. f = min/max. Pokud je pomer min/max >> 1 tak
  % to znamena, ze rozdiely indexov lokalnych maxim su priblizne rovnake. Pokial je pomer
  % min/max >> 0, potom rozdiely maxim su rozne. Otazka je, ze ako stanovit hranicu pomeru min/max.
  % Ale treba 0.75 je dobry kompromis. Idealne by bolo na zaklade velkeho poctu vzoriek napriklad
  % Monte Carlo simulace, tieto hranice nejak osahat a odvodit ich najpravdepodobnejsiu hodnotu.
  % Pripadne uvazovat realne data a z nich si urobit histogram pomerov a nejak cez percentily sa
  % rozhodnut, ze ako budem k charakteristike pristupovat.
  f = min(diff(idxUpp)) / max(diff(idxUpp));
  
  if (f >= 0.75)
    res = "categoryA"; % data maju "dominantnu" jednu periodu ("konstantna" frekvence)
  else
    res = "categoryB"; % data vykazuju viacej period nez len jedna dominantna
  end
  
end