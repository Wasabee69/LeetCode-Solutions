def getTwos(x):
    twos = 0
    while x&1 == 0:
        twos += 1
        x >>= 1
    return twos, x

def getFives(x):
    fives = 0
    while x % 5 == 0:
        fives += 1
        x //= 5
    return fives, x

def mult(a, b):
    x1, t1, f1 = a
    x2, t2, f2 = b
    return (x1*x2 % 10, t1+t2, f1+f2)
    
fac = [(1, 0, 0)]
for i in range(1, 1000):
    twos, x = getTwos(i)
    fives, x = getFives(x)
    fac.append(mult(fac[i-1], (x, twos, fives)))

class Solution:
    def triangularSum(self, nums: List[int]) -> int:
        n = len(nums)
        def divide(a, b):
            x1, t1, f1 = a
            x2, t2, f2 = b
            inv = [0, 1, 0, 7, 0, 0, 0, 3, 0, 9]
            return (x1 * inv[x2] % 10, t1-t2, f1-f2)

        def simplify(a):
            x, t, f = a
            cycle2 = [2, 4, 8, 6] # ends in 2, 4, 6, 8 -> 2, 4, 8, 16, 32, 64, 128
            cycle5 = [5] # Always ends in 5 -> 5, 25, 125, 625, 3125
            if t:
                x = x * cycle2[(t-1) % len(cycle2)]
            if f:
                x = x * cycle5[(f-1) % len(cycle5)]
            return x % 10

        def binomial(n, k):
            numerator = fac[n]
            denominator = mult(fac[k], fac[n-k])
            coeff = simplify(divide(numerator, denominator))
            return coeff

        res = 0
        for k in range(n):
            comb = binomial(n-1, k)
            res = (res + comb * nums[k]) % 10
        return res

        ##### Brute Force solution
        for i in range(n-1, 0, -1):
            p = nums[i]
            for j in range(i-1, -1, -1):
                np = nums[j]
                nums[j] = (nums[j] + p) % 10
                p = np
        return nums[0]
