import numpy as np

class Node:
    root = None
    action = ""
    state = np.array([])
    path_cost = 1
    depth = 0
    priority = 0 # the less the better
    created_index = 0

    def __init__(self, state, root, deep, action, created_index):
        self.root = root
        self.state = state
        self.depth = deep
        self.action = action
        self.created_index = created_index
