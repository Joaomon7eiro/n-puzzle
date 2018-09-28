import heapq

class PriorityQueue:

    def __init__(self):
        self.nodes_queue = []

    def push(self, node, ranking):
        best_node = ranking, node

        heapq.heappush(self.nodes_queue, best_node)

    def pop(self):
        ranking, node = heapq.heappop(self.nodes_queue)

        return node


