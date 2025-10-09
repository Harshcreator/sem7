#Write a program to implement matrix multiplication. Also implement multithreaded
#matrix multiplication with either one thread per row or one thread per cell. Analyze and compare
#their performance.

import threading
import time
import random

def generate_matrix(rows, cols):
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]

def matmul_standard(A, B):
    n, m, p = len(A), len(A[0]), len(B[0])
    result = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matmul_thread_row(A, B):
    n, m, p = len(A), len(A[0]), len(B[0])
    result = [[0] * p for _ in range(n)]
    def compute_row(i):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    threads = []
    for i in range(n):
        t = threading.Thread(target=compute_row, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return result

def matmul_thread_cell(A, B):
    n, m, p = len(A), len(A[0]), len(B[0])
    result = [[0] * p for _ in range(n)]
    def compute_cell(i, j):
        for k in range(m):
            result[i][j] += A[i][k] * B[k][j]
    threads = []
    for i in range(n):
        for j in range(p):
            t = threading.Thread(target=compute_cell, args=(i, j))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    return result

def matrices_equal(X, Y):
    return all(all(a == b for a, b in zip(row1, row2)) for row1, row2 in zip(X, Y))

if __name__ == "__main__":
    N = 100  # Adjust size for performance testing
    A = generate_matrix(N, N)
    B = generate_matrix(N, N)

    print("Running standard matrix multiplication...")
    start = time.time()
    result_std = matmul_standard(A, B)
    end = time.time()
    print(f"Standard: {end - start:.4f} seconds")

    print("Running multithreaded (per row)...")
    start = time.time()
    result_row = matmul_thread_row(A, B)
    end = time.time()
    print(f"Thread per row: {end - start:.4f} seconds")
    print("Results match:", matrices_equal(result_std, result_row))

    print("Running multithreaded (per cell)...")
    start = time.time()
    result_cell = matmul_thread_cell(A, B)
    end = time.time()
    print(f"Thread per cell: {end - start:.4f} seconds")
    print("Results match:", matrices_equal(result_std, result_cell))

    print("\nPerformance may vary based on matrix size and system capabilities.")
    
    
# Running standard matrix multiplication...
# Standard: 0.0665 seconds
# Running multithreaded (per row)...
# Thread per row: 0.0931 seconds
# Results match: True
# Running multithreaded (per cell)...
# Thread per cell: 1.1071 seconds
# Results match: True

# Performance may vary based on matrix size and system capabilities.