def binary_search(sorted_array, target):
    low = 0
    high = len(sorted_array) - 1
    iterations = 0

    while low <= high:
        mid = (low + high) // 2
        mid_value = sorted_array[mid]
        iterations += 1

        if mid_value < target:
            low = mid + 1
        elif mid_value > target:
            high = mid - 1
        else:
            return iterations, mid_value

    if high < 0:
        return iterations, None
    else:
        return iterations, sorted_array[low] if low < len(sorted_array) else None
