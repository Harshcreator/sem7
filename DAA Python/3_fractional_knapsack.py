def fractional_knapsack():
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    res = 0

    # Create list of (weight, value, ratio) and sort by ratio descending
    items = sorted(
        [(w, v, v / w) for w, v in zip(weights, values)],
        key=lambda x: x[2],
        reverse=True
    )

    for w, v, ratio in items:
        if capacity <= 0:
            break
        if w > capacity:
            res += capacity * ratio
            capacity = 0
        else:
            res += v
            capacity -= w
    print(int(res))

if __name__ == "__main__":
    fractional_knapsack()