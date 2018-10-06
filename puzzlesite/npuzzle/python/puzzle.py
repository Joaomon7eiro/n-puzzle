from .queue import PriorityQueue
from .node import Node
from .agent import Agent
from .functions import create_n_n_matrix, node_priority
import numpy as np


def main(string_array, dimension):

    # split the string array received from javascript to int list
    shuffled_state_array = [int(n) for n in string_array.split(",")]
    shuffled_state_matrix = np.reshape(shuffled_state_array, (dimension, dimension))

    # transform numpy array to list !NEED ATTENTION TO FIX LATER
    shuffled_state = shuffled_state_matrix.tolist()

    # creates the goal state based on the given dimension
    goal_state = create_n_n_matrix(dimension)

    agent = Agent()

    # creating start node with default params
    node = Node(shuffled_state, None, 0, "", 0)

    # defining the node priority
    node.priority = node_priority(node.state, goal_state)

    queue_node_priority = PriorityQueue()

    queue_node_priority.push(node, node.priority, node.created_index)

    all_nodes_created = []

    # count with the tentatives
    count_process = 0

    # the states that will be printed on html
    html_list = []

    while True:
        # pops the tested node that is not the goal
        node = queue_node_priority.pop()

        goal_success = agent.goal(node.state, goal_state)

        if goal_success:
            break

        queue_node_priority, all_nodes_created = agent.next(node, queue_node_priority, dimension,
                                                            goal_state, all_nodes_created)

        #print("no rank atual {} e acao {} e profundidade {}".format(node.priority, node.action, node.depth))
        #print("quantidade total {}".format(len(all_nodes_created)))

        count_process += 1

        if count_process == 1000:
            print("limite")

    print("contagem", count_process)

    html_list.append(node.state)

    try:
        while node.root.state != goal_state:

            html_list.insert(0, node.root.state)

            node = node.root
    except:
        print("final")

    return html_list

