function dataOut = kernelSmoother(dataIn, bandwidth)
  % KERNEL SMOOTHER je neparametricka metoda, ktora sluzi k aproximacii signalu a na neparametricky
  % odhad hustoty. 
  % Princip metody je zadokumentovany v tisicoch clankoch a knihach. Mne sa najviac pacila kniha od
  % Simonoff, Smoothing Methods in Statistics (https://www.springer.com/us/book/9780387947167) z
  % ktorej som cerpal najviac rozumu. V podstate sa jedna o lokalne neparametricke vyhladenie,
  % pricom parametre sa pocitaju v subsubore dat (v jadre - kernel).
  % Kernely/jadra, ktore maju specificke vlastnosti (spravanie sa na krajoch jadier a podobne), sa 
  % spocitaju roznymi pristupami. Najvyznamnejsie su Epancikovej jadro alebo Gaussovske jadro.
  % Momentalne je implementovane len gaussovsky pristup. Kvalita vyhladenia stoji a pada na volbe 
  % sirky jadra. Ak je sirka jadra velka, dostaneme hladky priebeh vyhladenia (bez detailov), ak je 
  % jadro male, metoda data aproximuje viacej podrobne. Existuje cela rada postupov ako ohdadnut 
  % optimalnu sirku jadra (zoznam vybranych postupov napr. v knihe Gromacki, A. (2018). 
  % "Nonparametric KernelDensity Estimation and ItsComputational Aspects", Springer). Knihovna
  % +DataSmoothing obsahuje len niektore z existujucich metod (Scott, Silverman ... )
  
  arguments
    dataIn (:,1) double {mustBeNonempty};
    bandwidth (1,1) double {mustBePositive};
  end
  
  nData = numel(dataIn);
  
  jadroMat = zeros(nData,nData); 
  normData = zeros(nData,nData); 
  kernel = fillKernel(dataIn, bandwidth); %par u (https://en.wikipedia.org/wiki/Kernel_(statistics))
  
  for i = 1:nData
    for j = 1:nData
      
      jadroMat(j,i) = getGaussConst * exp ( -1.0 * (kernel(j,i)^(2.0)) / 2.0 );
      normData(i,j) = dataIn(i) * jadroMat(j,i);
    end
  end
  
  sumJadroMat = sum(jadroMat);
  sumNormData = sum(normData);
  
  dataOut = zeros(nData,1);
  for i = 1:nData
    
    if sumJadroMat(i) == 0
      
      dataOut(i) = 0.0;
    else
      
      dataOut(i) = sumNormData(i) / sumJadroMat(i);
    end
  end
end

% loc
function D = fillKernel(data, h)
  
  n = length(data);
  X = 1:n;
  D = zeros(n,n);
  
  for i = 1:n
    
    for j = 1:n
      
      D(j,i) = (X(i) - X(j)) ./ h;
    end
  end
  
end

function GAUSS_CONST = getGaussConst()
  
  
  GAUSS_CONST = 1.0 / (2.0 * pi)^0.5;
end

