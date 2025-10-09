def recursive_fibonacci(n):
    if n<=1:
        return n
    else:
        return recursive_fibonacci(n-1) + recursive_fibonacci(n-2)

def non_recursive_fibonacci(n):
    first=0
    second=1
    print(first, end=' ')
    print(second, end=' ')
    count = n - 2
    while count > 0:
        third = first + second
        first=second
        second=third
        print(third, end=' ')
        count -= 1
    print()

if __name__=="__main__":
    n=10
    print("Recursive Fibonacci of", n, "is:")
    for i in range(n):
        print(recursive_fibonacci(i), end=' ')
    print()
    print("Non-Recursive Fibonacci of", n, "is:")
    non_recursive_fibonacci(n)
    
    
# Output:   
# Recursive Fibonacci of 10 is:
# 0 1 1 2 3 5 8 13 21 34 
# Non-Recursive Fibonacci of 10 is:
# 0 1 1 2 3 5 8 13 21 34 