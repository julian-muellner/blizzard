# FROM: Bayesian Inference using Data Flow Analysis; Claret et al.

types
    b : FiniteRange(0,1)
    c : FiniteRange(0,1)
end

b = 1
c = Bernoulli(1/2)
while c == 1:
    b = 1 - b
    c = Bernoulli(1/2)
end
