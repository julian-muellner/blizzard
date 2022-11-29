
types
    bound : FiniteRange(100,100)
    n : FiniteRange(1,200)
    f : FiniteRange(0,1)
    g : FiniteRange(0,300)
end

bound = 100
g = bound
while g >= bound:
    n = 1
    g = 0
    while n < bound:
        n = 2*n
        f = Bernoulli(0.5)
        if f == 1:
            g = 2*g
        else:
            g = 2*g+1
        end
    end
end
