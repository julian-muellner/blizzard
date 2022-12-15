# FROM: Bayesian Inference using Data Flow Analysis; Claret et al.

types
    c1 : FiniteRange(0,1)
    c2 : FiniteRange(0,1)
end

c1 = Bernoulli(1/2)
c2 = Bernoulli(1/2)
while !((c1 == 1) || (c2 == 1)):
    c1 = Bernoulli(1/2)
    c2 = Bernoulli(1/2)
end
