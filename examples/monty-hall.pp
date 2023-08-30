
types
    car : FiniteRange(1,3)
    selected : FiniteRange(1,3)
    revealed : FiniteRange(0,3)
    switch : FiniteRange(0,1)
    success : FiniteRange(0,1)
end

car = DiscreteUniform(1,3)
selected = DiscreteUniform(1,3)
if car == 1:
    if selected == 1:
        revealed = DiscreteUniform(2,3)
    else:
        if selected == 2:
            revealed = 3
        else:
            revealed = 2
        end
    end
else:
    if car == 2:
        if selected == 1:
            revealed = 3
        else:
            if selected == 2:
                revealed = Categorical(1/2, 0, 1/2)
                revealed = 1 + revealed
            else:
                revealed = 1
            end
        end
    else:
        if selected == 1:
            revealed = 2
        else:
            if selected == 2:
                revealed = 1
            else:
                revealed = DiscreteUniform(1,2)
            end
        end
    end
end

# if switch, pick the door that is neither selected, nor revealed
switch = Bernoulli(p)
if switch == 1:
    if !((selected == 1) || (revealed == 1)):
        selected = 1
    else:
        if !((selected == 2) || (revealed == 2)):
            selected = 2
        else:
            selected = 3
        end
    end
end

if selected == car:
    success = 1
else:
    success = 0
end



