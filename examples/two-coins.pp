# FROM: Bayesian Inference using Data Flow Analysis; Claret et al.
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/r2/twoCoins.psi

types
    c1 : FiniteRange(0,1)
    c2 : FiniteRange(0,1)
end

c1 = Bernoulli(1/2)
c2 = Bernoulli(1/2)
observe (c1 == 1) || (c2 == 1)
