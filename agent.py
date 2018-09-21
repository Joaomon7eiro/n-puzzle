from functions import find_number_row_and_col, next_node, search_equal_state, ranking


class Agent:

    def goal(self, list, goal_list):

        if list == goal_list:
            return True
        else:
            return False

    def next(self, node, list, dimension, goal_state):

        dimension -= 1

        row_0, col_0 = find_number_row_and_col(node.state, 0)

        child_list = []

        if row_0 > 0:
            node1 = next_node(node, row_0, col_0, row_0 - 1, col_0, "up")
            found = search_equal_state(node1.state, list)
            if not found:
                child_list.append(node1)
        if row_0 < dimension:
            node2 = next_node(node, row_0, col_0, row_0 + 1, col_0, "down")
            found = search_equal_state(node2.state, list)
            if not found:
                child_list.append(node2)
        if col_0 > 0:
            node3 = next_node(node, row_0, col_0, row_0, col_0 - 1, "left")
            found = search_equal_state(node3.state, list)
            if not found:
                child_list.append(node3)
        if col_0 < dimension:
            node4 = next_node(node, row_0, col_0, row_0, col_0 + 1, "right")
            found = search_equal_state(node4.state, list)
            if not found:
                child_list.append(node4)

        child_list = ranking(child_list, goal_state)

        return list + child_list