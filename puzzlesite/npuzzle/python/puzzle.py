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

    while True:
        # pops the tested node that is not the goal
        if search_type_choice == '5':
            node = node_list.pop()
        else:
            node = node_list.pop(search_type)

        goal_success = agent.goal(node.state, goal_state)

        if goal_success:
            break

        node_list, all_nodes_created = agent.next(node, node_list, dimension, goal_state, all_nodes_created,
                                                  search_type_choice)

        #print("no rank atual {} e acao {} e profundidade {}".format(node.priority, node.action, node.depth))
        #print("quantidade total {}".format(len(all_nodes_created)))

        count_process += 1

        if search_type_choice == '3':
            if count_process == 1000:
                print("limite")
                break

    print("contagem", count_process)

    print("--- %s seconds ---" % (time.time() - start_time))

    html_list.append(node.state)

    try:
        while node.root.state != goal_state:

            html_list.insert(0, node.root.state)

            node = node.root
    except:
        print("final")

    return html_list

