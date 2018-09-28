from .queue import Priority_Queue
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
    node = Node(shuffled_state, None, 0, "")

    # defining the node priority
    node.priority = node_priority(node.state, goal_state)

    node_priority_queue = Priority_Queue()

    node_priority_queue.push(node, node.priority)
    #node_list = []

    all_nodes_created = []

    #node_priority_queue.append(node)

    goal_success = agent.goal(node.state, goal_state)

    # count with the tentatives
    count_process = 0

    # the states that will be printed on html
    html_list = []

    while not goal_success:
        # pops the tested node that is not the goal
        node_priority_queue.pop()

        node_priority_queue, all_nodes_created = agent.next(node, node_priority_queue, dimension,
                                                            goal_state, all_nodes_created)

        #node_priority_queue = sorted(node_priority_queue, key=lambda node_list: node_list.priority, reverse=False)

        for index, top_node in enumerate(node_priority_queue):
            print("priority {}, profundidade {}".format(top_node.priority, top_node.depth))
            if index == 10:
                break

        print("tamanho da lista".format(len(node_priority_queue)))
        node = node_priority_queue[0]
        goal_success = agent.goal(node.state, goal_state)

        print("no rank atual {} e acao {}".format(node.priority, node.action))

        count_process += 1

    print("contagem", count_process)

    html_list.append(node.state)

    try:
        while node.root.state != goal_state:

            html_list.insert(0, node.root.state)

            node = node.root
    except:
        print("final")

    return html_list

