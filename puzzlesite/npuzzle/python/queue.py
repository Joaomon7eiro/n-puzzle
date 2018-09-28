import heapq

class Priority_Queue:

    def __init__(self):
        self.nodes_queue = []

    def push(self, node, priority):
        best_node = priority, node

        heapq.heappush(self.nodes_queue, best_node)

    def pop(self):
        (priority, node) = heapq.heappop(self.nodes_queue)

        return node

