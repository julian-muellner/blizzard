# FROM: Bayesian Inference using Data Flow Analysis; Claret et al.
# Compute uniform probability between 0 and bound - 1

types
    bound : FiniteRange(20,20)
    n : FiniteRange(1,40)
    f : FiniteRange(0,1)
    g : FiniteRange(0,60)
end

bound = 20
g = bound
while g >= bound:
    n = 1
    g = 0
    while n < bound:
        n = 2*n
        f = Bernoulli(1/2)
        if f == 1:
            g = 2*g
        else:
            g = 2*g+1
        end
    end
end
