import numpy as np
import heapq
import random

class MultiHeap:
    def __init__(self, n, d):
        self.queues = np.array(n)
        self.sizes = np.array(n)
        self.d = d
        for i in range(n):
            self.queues[n] = []
            self.sizes[n] = 0

    def push(self, item):
        queue = min()
        heapq.heappush(, item)
