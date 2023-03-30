
types
    x : FiniteRange(-1,12)
    f : FiniteRange(0,1)
    z : FiniteRange(1,3)
end

x = 4
while x > 0 && x < 10:
    f = Bernoulli(1/3)
    if f == 1:
        z = DiscreteUniform(1,3)
        x = x + z
    else:
        x = x - 2
    end
end
