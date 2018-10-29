from .functions import find_number_row_and_col, search_equal_state, node_priority
import numpy as np
from .node import Node


class Agent:

    def goal(self, current_state, goal_state):

        if np.array_equal(current_state, goal_state):
            return True
        else:
            return False

    def next(self, node, node_list, dimension):

        dimension -= 1

        row_0, col_0 = find_number_row_and_col(node.state, 0)

        if row_0 > 0:
            node_down = self.move_node(node, row_0, col_0, row_0 - 1, col_0, "down", 0)
            node_list.append(node_down)

        if row_0 < dimension:
            node_up = self.move_node(node, row_0, col_0, row_0 + 1, col_0, "up", 0)
            node_list.append(node_up)

        if col_0 > 0:
            node_right = self.move_node(node, row_0, col_0, row_0, col_0 - 1, "right", 0)
            node_list.append(node_right)

        if col_0 < dimension:
            node_left = self.move_node(node, row_0, col_0, row_0, col_0 + 1, "left", 0)
            node_list.append(node_left)

        return node_list

    def nextHeuristic(self, node, node_list, dimension, goal_state, count, search_type, all_nodes_created=None):

        dimension -= 1

        row_0, col_0 = find_number_row_and_col(node.state, 0)

        if row_0 > 0:
            node_down = self.move_node(node, row_0, col_0, row_0 - 1, col_0, "down", count)
            count += 1
            node_down.priority = node_priority(node_down.state, goal_state, search_type, node.depth)

            find = search_equal_state(node_down, all_nodes_created)

            if not find:
                node_list.push(node_down, node_down.priority, node_down.created_index)
                all_nodes_created.append(node_down)

        if row_0 < dimension:
            node_up = self.move_node(node, row_0, col_0, row_0 + 1, col_0, "up", count)
            count += 1
            node_up.priority = node_priority(node_up.state, goal_state, search_type, node.depth)

            find = search_equal_state(node_up, all_nodes_created)

            if not find:
                node_list.push(node_up, node_up.priority, node_up.created_index)
                all_nodes_created.append(node_up)

        if col_0 > 0:
            node_right = self.move_node(node, row_0, col_0, row_0, col_0 - 1, "right", count)
            count += 1
            node_right.priority = node_priority(node_right.state, goal_state, search_type, node.depth)

            find = search_equal_state(node_right, all_nodes_created)

            if not find:
                node_list.push(node_right, node_right.priority, node_right.created_index)
                all_nodes_created.append(node_right)

        if col_0 < dimension:
            node_left = self.move_node(node, row_0, col_0, row_0, col_0 + 1, "left", count)
            count += 1
            node_left.priority = node_priority(node_left.state, goal_state, search_type, node.depth)

            find = search_equal_state(node_left, all_nodes_created)

            if not find:
                node_list.push(node_left, node_left.priority, node_left.created_index)
                all_nodes_created.append(node_left)

        return node_list, count, all_nodes_created

    @staticmethod
    def move_node(node, row_0, col_0, new_value_row, new_value_col, action, index):

        new_list = np.copy(node.state)
        new_list[row_0, col_0] = new_list[new_value_row, new_value_col]
        new_list[new_value_row, new_value_col] = 0
        node = Node(new_list, node, node.depth + 1, action, index)
        return node

