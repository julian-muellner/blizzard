# FROM: Infer.NET
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/fun/murderMysteryEq.psi

types
    gunfound : FiniteRange(0,1)
    alicedunnit : FiniteRange(0,1)
    withgun : FiniteRange(0,1)
end

gunfound = 1
alicedunnit = Bernoulli(3/10)
if alicedunnit == 1:
    withgun = Bernoulli(3/100)
else:
    withgun = Bernoulli(8/10)
end

observe (withgun == gunfound)

# --analyze alicedunnit; // expected: 9/569 alicedunnit == 1, 560/569 alicedunnit == 0
