# FROM: Bayesian Networks.
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/r2/burglarAlarm.psi

types
    burglary : FiniteRange(0,1)
    earthquake : FiniteRange(0,1)
    marywakes : FiniteRange(0,1)
    phoneworking : FiniteRange(0,1)
end

burglary = Bernoulli(1/1000)
earthquake = Bernoulli(1/10000) 

if earthquake == 1:
    phoneworking = Bernoulli(7/10)
else:
    phoneworking = Bernoulli(99/100)
end

if earthquake == 1:
    marywakes = Bernoulli(80/100)
else:
    if burglary == 1:
        marywakes = Bernoulli(60/100)
    else:
        marywakes = Bernoulli(20/100)
    end
end

observe (marywakes == 1) && (phoneworking == 1)
 