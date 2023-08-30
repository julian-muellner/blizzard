types
    s : FiniteRange(0,15)
    i : FiniteRange(0,2)
    f : FiniteRange(0,1)
end

s = 0
f = 1
while s < 3 && f == 1:
    f = Bernoulli(p)
    i = DiscreteUniform(0,2)
    s = s + i
end
