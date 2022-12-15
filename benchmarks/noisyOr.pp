# FROM: DICE, PSI.
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/r2/noisyOrModel.psi
# DICE Implementation: https://github.com/SHoltzen/dice/blob/master/benchmarks/baselines/noisyOr.dice

types
    nzero : FiniteRange(0,1)
    none : FiniteRange(0,1)
    ntwo : FiniteRange(0,1)
    nthree : FiniteRange(0,1)
    nfour : FiniteRange(0,1)
    ntwoone : FiniteRange(0,1)
    nthreethree : FiniteRange(0,1)
    ntwotwo : FiniteRange(0,1)
    nthreeone : FiniteRange(0,1)
    nthreetwo : FiniteRange(0,1)
end

nzero = Bernoulli(5/10)
nfour = Bernoulli(5/10)

none = 0
ntwoone = 0
nthreethree = 0
ntwotwo = 0
nthreeone = 0
nthreetwo = 0

if nzero == 1:
    none = Bernoulli(4/5)
    ntwoone = Bernoulli(4/5)
else:
    none = Bernoulli(1/10)
    ntwoone = Bernoulli(1/10)
end

if nfour == 1:
    ntwotwo = Bernoulli(4/5)
    nthreethree = Bernoulli(4/5)
else:
    ntwotwo = Bernoulli(1/10)
    nthreethree = Bernoulli(1/10)
end

if ntwoone == 0 && ntwotwo == 0:
    ntwo = 0
else:
    ntwo = 1
end

if none == 1:
    nthreeone = Bernoulli(4/5)
else:
    nthreeone = Bernoulli(1/10)
end

if ntwo == 1:
    nthreetwo = Bernoulli(4/5)
else:
    nthreetwo = Bernoulli(1/10)
end

if nthreeone == 0 && nthreetwo == 0 && nthreethree == 0:
    nthree = 0
else:
    nthree = 1
end

#--analyze nthree
