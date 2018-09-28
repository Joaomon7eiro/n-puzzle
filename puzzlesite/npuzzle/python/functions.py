from copy import deepcopy
from .node import Node
from numpy import *


def node_priority(node_state, goal_state):
    priority = 0

    for row_values in node_state:

        for value in row_values:
            if value == 0:
                continue
            value_row, value_col = find_number_row_and_col(node_state, value)
            goal_row, goal_col = find_number_row_and_col(goal_state, value)

            if goal_row >= value_row:
                priority += goal_row - value_row
            else:
                priority += value_row - goal_row

            if goal_col >= value_col:
                priority += goal_col - value_col
            else:
                priority += value_col - goal_col

    return priority


def search_equal_state(child_node, all_nodes):
    for node in all_nodes:
        if node.state == child_node.state:
            return True

    return False


def find_number_row_and_col(state, number):
    number_row, number_col = 0, 0
    for index_row, row in enumerate(state):
        for index_col, value in enumerate(row):
            if value == number:
                number_row, number_col = index_row, index_col
                break

    return number_row, number_col


def create_n_n_matrix(dimension):

    goal_list = range(1, dimension*dimension + 1)

    goal_list = reshape(goal_list, (dimension, dimension))
    goal_list[-1][-1] = 0

    goal_state = goal_list.tolist()
    return goal_state


def format_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def move_node(node, row_0, col_0, new_value_row, new_value_col, action, index):
    new_list = deepcopy(node.state)
    new_list[row_0][col_0] = new_list[new_value_row][new_value_col]
    new_list[new_value_row][new_value_col] = 0
    node = Node(new_list, node, node.depth + 1, action, index)
    return node
