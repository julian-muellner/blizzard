# FROM: Infer.NET
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/fun/evidence/model1.psi

types
    evidence : FiniteRange(0,1)
    coin : FiniteRange(0,1)
end

evidence = Bernoulli(1/2)
if evidence == 1:
    coin = Bernoulli(1/2)
    observe (coin == 1)
end

# --analyze evidence; // expected: 1/3 evidence == 1, 2/3 evidence == 0
