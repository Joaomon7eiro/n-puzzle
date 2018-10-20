from .node import Node
import numpy as np


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


def state_disogarnized(node_state, goal_state):

    count = 0

    for row_values in node_state:

        for value in row_values:
            if value == 0:
                continue
            value_row, value_col = find_number_row_and_col(node_state, value)
            goal_row, goal_col = find_number_row_and_col(goal_state, value)

            if value_col != goal_col or value_row != goal_row:
                count += 1

    return count


def search_equal_state(child_node, all_nodes):

    for node in all_nodes:
        if np.array_equal(node.state, child_node.state):
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

    goal_list = np.arange(1, dimension*dimension + 1).reshape(dimension, dimension)
    goal_list[-1, -1] = 0

    return goal_list


def move_node(node, row_0, col_0, new_value_row, new_value_col, action, index):

    new_list = np.copy(node.state)
    new_list[row_0, col_0] = new_list[new_value_row, new_value_col]
    new_list[new_value_row, new_value_col] = 0
    node = Node(new_list, node, node.depth + 1, action, index)
    return node
