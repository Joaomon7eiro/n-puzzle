class Node:
    root = None
    action = ""
    state = []
    path_cost = 1
    depth = 0
    priority = 0 #the less the better

    def __init__(self, list, root, deep, action):
        self.root = root
        self.state = list
        self.depth = deep
        self.action = action
