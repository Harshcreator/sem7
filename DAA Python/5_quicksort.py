import random, time

def quicksort(arr, low, high, cmp, rand=False):
    if low < high:
        p, cmp[0] = partition(arr, low, high, cmp[0], rand)
        quicksort(arr, low, p-1, cmp, rand)
        quicksort(arr, p+1, high, cmp, rand)

def partition(arr, low, high, cmp, rand):
    if rand:
        r = random.randint(low, high)
        arr[high], arr[r] = arr[r], arr[high]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        cmp += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1, cmp

def analyze(arr):
    for name, rand in [('Deterministic', False), ('Randomized', True)]:
        a = arr[:]
        cmp = [0]
        t0 = time.time()
        quicksort(a, 0, len(a)-1, cmp, rand)
        t1 = time.time()
        print(f"{name} QuickSort: Comparisons={cmp[0]}, Time={t1-t0:.6f}s, Sorted={a}")

if __name__ == "__main__":
    arr = [random.randint(1, 100) for _ in range(10)]
    print("Original:", arr)
    analyze(arr)
    
# Example Output:
# Original: [90, 13, 42, 69, 94, 64, 64, 49, 51, 64]
# Deterministic QuickSort: Comparisons=21, Time=0.000011s, Sorted=[13, 42, 49, 51, 64, 64, 64, 69, 90, 94]
# Randomized QuickSort: Comparisons=29, Time=0.000015s, Sorted=[13, 42, 49, 51, 64, 64, 64, 69, 90, 94]