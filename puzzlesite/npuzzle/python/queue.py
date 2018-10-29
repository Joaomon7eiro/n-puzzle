import heapq


class PriorityQueue:

    def __init__(self):
        self.nodes_queue = []

    def push(self, node, priority, index):
        new_node = priority, index, node

        heapq.heappush(self.nodes_queue, new_node)

    def pop(self):
        priority, index, node = heapq.heappop(self.nodes_queue)

        return node

