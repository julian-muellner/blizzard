#!/usr/bin/env python3
import random
from statistics import NormalDist

def process():
    s = 0
    f = True

    while s < 1 and f == True:
        f = (random.random() <= p)
        s += random.randint(0,2)
        
    x = random.uniform(0, s)

    print(f"x: {x} \t s: {s}")

if __name__ == "__main__":
    random.seed(42)
    p = 0.7
    
    print(f"p: {p}")
    
    for i in range(10):
        process()