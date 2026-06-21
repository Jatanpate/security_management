def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        print(f"printing mid {mid}")

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
            print(f"printing left {left}")
        else:
            right = mid - 1
            print(f"printing right {right}")
    return -1

nums = [2, 4, 6, 8, 10, 12]

print(binary_search(nums, 8))   # 3
print(binary_search(nums, 7))   # -1



