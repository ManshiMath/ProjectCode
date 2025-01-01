import math
def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, math.sqrt(n)):
        if n % i == 0 and n != i:
            return False
    return True

n = 4
while True:
    find = False
    for a in range(2, n/2):
        b = n - a
        if isPrime(a) and isPrime(b):
            find = True
            break
    
    if not find:
        break
    else:
        n += 2


