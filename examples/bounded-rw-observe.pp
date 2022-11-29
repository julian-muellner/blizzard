
types
    x : FiniteRange(-1,12)
    f : FiniteRange(0,1)
    z : FiniteRange(1,3)
end

x = 4
while x > 0 && x < 5:
    f = Bernoulli(p)
    if f == 1:
        z = DiscreteUniform(1,3)
        x = x + z
    else:
        x = x - 2
    end
    observe x < 4 
end
