from .functions import find_number_row_and_col, move_node, search_equal_state, node_priority
import numpy as np


class Agent:

    def goal(self, current_state, goal_state):

        if np.array_equal(current_state, goal_state):
            return True
        else:
            return False

    def next(self, node, node_list, dimension, goal_state, all_nodes_created, search_type_choice):

        dimension -= 1

        row_0, col_0 = find_number_row_and_col(node.state, 0)

        if row_0 > 0:
            node_down = move_node(node, row_0, col_0, row_0 - 1, col_0, "down", len(all_nodes_created))
            node_down.priority = node_priority(node_down.state, goal_state)

            if search_type_choice == "5":
                found = search_equal_state(node_down, all_nodes_created)
                if not found:
                    node_list.push(node_down, node_down.priority, node_down.created_index)
            else:
                node_list.append(node_down)

            all_nodes_created.append(node_down)

        if row_0 < dimension:
            node_up = move_node(node, row_0, col_0, row_0 + 1, col_0, "up", len(all_nodes_created))
            node_up.priority = node_priority(node_up.state, goal_state)

            if search_type_choice == "5":
                found = search_equal_state(node_up, all_nodes_created)
                if not found:
                    node_list.push(node_up, node_up.priority, node_up.created_index)
            else:
                node_list.append(node_up)

            all_nodes_created.append(node_up)

        if col_0 > 0:
            node_right = move_node(node, row_0, col_0, row_0, col_0 - 1, "right", len(all_nodes_created))
            node_right.priority = node_priority(node_right.state, goal_state)

            if search_type_choice == "5":
                found = search_equal_state(node_right, all_nodes_created)
                if not found:
                    node_list.push(node_right, node_right.priority, node_right.created_index)
            else:
                node_list.append(node_right)

            all_nodes_created.append(node_right)

        if col_0 < dimension:
            node_left = move_node(node, row_0, col_0, row_0, col_0 + 1, "left", len(all_nodes_created))
            node_left.priority = node_priority(node_left.state, goal_state)

            if search_type_choice == "5":
                found = search_equal_state(node_left, all_nodes_created)
                if not found:
                    node_list.push(node_left, node_left.priority, node_left.created_index)
            else:
                node_list.append(node_left)

            all_nodes_created.append(node_left)

        return node_list, all_nodes_created
