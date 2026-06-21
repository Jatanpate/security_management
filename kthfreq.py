import heapq
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)
    min_heap = []

    for num, freq in count.items():
        heapq.heappush(min_heap, (freq, num))
        print(min_heap)

        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return [num for freq, num in min_heap]

nums = [1, 1, 1, 2, 2, 3]

print(top_k_frequent(nums, 2))