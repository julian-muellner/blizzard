# FROM: Bayesian Networks.
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/r2/grass.psi

types
    tmptwo : FiniteRange(0,1)
    tmpthree : FiniteRange(0,1)
    cloudy : FiniteRange(0,1)
    rain : FiniteRange(0,1)
    sprinkler : FiniteRange(0,1)
end

cloudy = Bernoulli(5/10)

if cloudy == 1:
    rain = Bernoulli(8/10)
    sprinkler = Bernoulli(1/10)
else:
    rain = Bernoulli(2/10)
    sprinkler = Bernoulli(5/10)
end

tmptwo = Bernoulli(9/10)
tmpthree = Bernoulli(9/10)

observe ((rain == 1) && (tmptwo == 1)) || ((tmpthree == 1) && (sprinkler == 1)) 
