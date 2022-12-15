# FROM: Infer.NET
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/fun/evidence/model2.psi

types
    evidence : FiniteRange(0,1)
    coin : FiniteRange(0,1)
    coinone : FiniteRange(0,1)
end

evidence = Bernoulli(1/2)
if evidence == 1:
    coinone = Bernoulli(1/2)
    observe (coinone == 1)
    coin = coinone
else:
    coin = Bernoulli(1/2)
end

# --analyze coin; // expected: 1/3 coin == 0, 2/3 evidence == 1
