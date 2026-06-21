import heapq

def top_k_largest(nums, k):
    min_heap = []

    for num in nums:
        heapq.heappush(min_heap, -num)
        print(min_heap)

        if len(min_heap) > k:
            heapq.heappop(min_heap)
            print(" inside if loop")
            print(min_heap)

    return [-x for x in min_heap]

nums = [3, 1, 5, 12, 2, 11]

print(top_k_largest(nums, 1))