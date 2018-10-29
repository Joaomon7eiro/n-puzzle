from .queue import PriorityQueue
from .node import Node
from .agent import Agent
from .functions import node_priority
import numpy as np
import time

from pympler.asizeof import asizeof


def create_n_n_matrix(dimension):

    goal_list = np.arange(1, dimension*dimension + 1).reshape(dimension, dimension)
    goal_list[-1, -1] = 0

    return goal_list


def breadth_search(agent, shuffled_state, goal_state, count_process, dimension):

    node = Node(shuffled_state, None, 0, "", 0)

    node_list = list()
    node_list.append(node)

    while True:
        node = node_list.pop(0)

        goal_success = agent.goal(node.state, goal_state)

        count_process += 1

        #print("acao {} profundidade {}".format(node.action, node.depth))

        if goal_success:
            break

        node_list = agent.next(node, node_list, dimension)

    return node, count_process


def depth_search(agent, shuffled_state, goal_state, count_process, dimension, search_type_choice, limit):
    node = Node(shuffled_state, None, 0, "", 0)

    node_list = list()
    node_list.append(node)
    if search_type_choice == '3':
        if limit == '':
            limit = 0
        else:
            limit = int(limit)

    if search_type_choice == '4':
        limit = 1

    while True:

        if len(node_list) == 0:
            print('-----------------------chegou no limite e nao encontrou o resultado-----------------------')
            if search_type_choice == '3':
                break
            else:
                limit += 1
                print('-----------------------excluiu a lista e aumentou o limite(limite atualizado = {})-----------------------'.format(limit))

                node = Node(shuffled_state, None, 0, "", 0)

                node_list.append(node)
                print(asizeof(node_list))

        node = node_list.pop()

        goal_success = agent.goal(node.state, goal_state)

        count_process += 1

        #print("acao {} profundidade {}".format(node.action, node.depth))

        if goal_success:
            break

        if (search_type_choice == '3' or search_type_choice == '4') and node.depth == limit:
            continue

        node_list = agent.next(node, node_list, dimension)

    return node, count_process


def heuristic_search(agent, shuffled_state, goal_state, count_process, dimension, search_type):

    count = 1

    node = Node(shuffled_state, None, 0, "", 0)

    # defining the node priority
    node.priority = node_priority(node.state, goal_state, search_type, node.depth)

    node_list = PriorityQueue()
    node_list.push(node, node.priority, 0)
    while True:

        node = node_list.pop()

        goal_success = agent.goal(node.state, goal_state)

        count_process += 1

        # print("acao {} profundidade {}".format(node.action, node.depth))

        if goal_success:
            break

        node_list, count = agent.nextHeuristic(node, node_list, dimension, goal_state, count,
                                               search_type)

    return node, count_process


def main(string_array, dimension, search_type_choice, limit):

    start_time = time.time()
    # split the string array received from javascript to int np array
    shuffled_state_array = [int(n) for n in string_array.split(",")]
    shuffled_state = np.reshape(shuffled_state_array, (dimension, dimension))

    shuffled_state = np.array([
        [4, 0, 2],
        [5, 6, 8],
        [1, 7, 3]
    ])

    # creates the goal state based on the given dimension
    goal_state = create_n_n_matrix(dimension)

    agent = Agent()

    # count with the tentatives
    count_process = 0

    # the states that will be printed on html
    html_list = []

    if search_type_choice == '1':
        node, count_process = breadth_search(agent, shuffled_state, goal_state, count_process, dimension)
    elif search_type_choice == '2':
        node, count_process = depth_search(agent, shuffled_state, goal_state, count_process, dimension, '2', limit)
    elif search_type_choice == '3':
        node, count_process = depth_search(agent, shuffled_state, goal_state, count_process, dimension, '3', limit)
    elif search_type_choice == '4':
        node, count_process = depth_search(agent, shuffled_state, goal_state, count_process, dimension, '4', limit)
    elif search_type_choice == '5':
        node, count_process = heuristic_search(agent, shuffled_state, goal_state, count_process, dimension, "1")
    elif search_type_choice == '6':
        node, count_process = heuristic_search(agent, shuffled_state, goal_state, count_process, dimension, "2")
    elif search_type_choice == '7':
        # A*
        node, count_process = heuristic_search(agent, shuffled_state, goal_state, count_process, dimension, "3")
    else:
        # Uniform cost
        node, count_process = heuristic_search(agent, shuffled_state, goal_state, count_process, dimension, "4")

    time_spent = time.time() - start_time

    html_list.append(node.state.tolist())

    try:
        while not np.array_equal(node.root.state, goal_state):
            html_list.insert(0, node.root.state.tolist())
            node = node.root
    except:
        print("final")

    total_steps = len(html_list)-1
    return html_list, count_process, time_spent, total_steps

