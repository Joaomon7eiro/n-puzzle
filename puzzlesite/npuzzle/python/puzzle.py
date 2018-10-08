from .queue import PriorityQueue
from .node import Node
from .agent import Agent
from .functions import create_n_n_matrix, node_priority
import numpy as np
import time


def main(string_array, dimension, search_type_choice):
    start_time = time.time()
    # split the string array received from javascript to int list
    shuffled_state_array = [int(n) for n in string_array.split(",")]
    shuffled_state = np.reshape(shuffled_state_array, (dimension, dimension))

    # creates the goal state based on the given dimension
    goal_state = create_n_n_matrix(dimension)

    agent = Agent()

    # creating start node with default params
    node = Node(shuffled_state, None, 0, "", 0)

    # defining the node priority
    node.priority = node_priority(node.state, goal_state)

    if search_type_choice == '5':
        node_list = PriorityQueue()
        node_list.push(node, node.priority, node.created_index)
    else:
        node_list = list()
        node_list.append(node)

    all_nodes_created = []

    # count with the tentatives
    count_process = 0

    # the states that will be printed on html
    html_list = []

    if search_type_choice == '1':
        search_type = 0
    else:
        search_type = -1

    iterative = 10
    while True:
        count_process += 1

        if search_type_choice != '5':
            if len(node_list) < 1:
                if search_type_choice == '3':
                    break
                else:
                    print('zerou')
                    iterative *= 2
                    node = Node(shuffled_state, None, 0, "", 0)
                    node.priority = node_priority(node.state, goal_state)
                    node_list = list()
                    node_list.append(node)

        # pops the tested node that is not the goal
        if search_type_choice == '5':
            node = node_list.pop()
        else:
            node = node_list.pop(search_type)

        goal_success = agent.goal(node.state, goal_state)

        if goal_success:
            break

        if (search_type_choice == '3' or search_type_choice == '4') and node.depth + 1 == iterative:
            continue

        node_list, all_nodes_created = agent.next(node, node_list, dimension, goal_state, all_nodes_created,
                                                  search_type_choice)

    print("contagem", count_process)

    print("--- %s segundos ---" % (time.time() - start_time))

    html_list.append(node.state.tolist())
    try:
        while not np.array_equal(node.root.state, goal_state):
            html_list.insert(0, node.root.state.tolist())

            node = node.root
    except:
        print("final")

    return html_list
