import numpy as np


def node_priority(node_state, goal_state, search_type, node_depth=None):

    priority = 0
    count = 0

    for row_values in node_state:

        for value in row_values:
            if value == 0:
                continue
            value_row, value_col = find_number_row_and_col(node_state, value)
            goal_row, goal_col = find_number_row_and_col(goal_state, value)

            if value_col != goal_col or value_row != goal_row:
                count += 1

            if goal_row >= value_row:
                priority += goal_row - value_row
            else:
                priority += value_row - goal_row

            if goal_col >= value_col:
                priority += goal_col - value_col
            else:
                priority += value_col - goal_col

    if search_type == '1':
        return priority
    elif search_type == '2':
        return count
    else:
        # A*
        return priority + node_depth


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



