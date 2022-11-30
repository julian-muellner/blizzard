
types
    x : FiniteRange(-2,12)
    y : FiniteRange(-1,12)
    f : FiniteRange(0,1)
    z : FiniteRange(1,3)
end

x = 3
y = 2
while x >= 0 && y >= 0 && x <= 5 && y <= 5:
    f = Bernoulli(4/10)
    if f == 1:
        z = DiscreteUniform(1,3)
        x = x + z
    else:
        x = x - 2
    end
    
    f = Bernoulli(5/10)
    if f == 1:
        y = y + 1
    else:
        y = y - 1
    end
end
