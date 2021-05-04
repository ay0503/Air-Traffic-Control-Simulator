#! PSEUDOCODE
# extract the digit
# 24567 % 10 2456 + 7
# 24567 // 10 = 2456
# extract the next digit
# == return True
# 

def hasConsecutiveDigits(n):
    while n > 0:
        digit = n % 10
        n //= 10
        newDigit = n % 10
        if digit == newDigit:
            return True

def isPerfectNumber(n):
    for divisor in range(1, n):
        if n % divisor == 0:
            sum += divisor
    return sum == n

def nthPerfectNumber(n):
    count = 0
    currNum = 0
    while count <= n:
        currNum += 1
        if isPerfectNumber(currNum):
            count += 1
    return currNum

#! 1. prime number
#! 2. sum of its digits are also prime

# n is factor if n % k == 0 

def isPrime(n):
    if n == 0 or n == 1:
        return False
    for k in range(2, n):
        if n % k == 0:
            return False
    return True

# find digit, and sum
def sumDigits(n):
    pass