import time

def f(n):
    return int((time.time()//604800-2918+n)%6)

print(f(7))