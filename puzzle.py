import copy
from random import randint
#from numpy import *


def ranking(node_list, goal):

    ranking_nodes = []
    best_ranking = 100

    for node in node_list:

        ranking = 0
        for row_values in node.state:

            for value in row_values:
                if value == 0:
                    continue
                value_row, value_col = find_number_row_and_col(node.state, value)
                goal_row, goal_col = find_number_row_and_col(goal, value)


                if goal_row >= value_row:
                    ranking += goal_row - value_row
                else:
                    ranking += value_row - goal_row

                if goal_col >= value_col:
                    ranking += goal_col - value_col
                else:
                    ranking += value_col - goal_col

        if ranking < best_ranking:
            best_ranking = ranking

        node.ranking = ranking

    for node in node_list:
        if node.ranking == best_ranking:
            ranking_nodes.append(node)

    return ranking_nodes


def search_equal_state(state, list):
    for node in list:
        if node.state == state:
            return True

    return False


def find_number_row_and_col(list, number):
    number_row, number_col = 0, 0
    for index_row, row in enumerate(list):
        for index_col, value in enumerate(row):
            if value == number:
                number_row, number_col = index_row, index_col
                break

    return number_row, number_col

# def create_n_n_matrix(dimension):
#
#     x = range(1, dimension*dimension + 1)
#
#     x = reshape(x, (dimension, dimension))
#     x[-1][-1] = 0
#
#     return x


def format_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


class Agent:
    def next_node(self, node, row_0, col_0, new_value_row, new_value_col, action):
        new_list = copy.deepcopy(node.state)
        new_list[row_0][col_0] = new_list[new_value_row][new_value_col]
        new_list[new_value_row][new_value_col] = 0
        node = Node(new_list, node, node.depth + 1, action)
        return node

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
            node1 = self.next_node(node, row_0, col_0, row_0 - 1, col_0, "up")
            found = search_equal_state(node1.state, list)
            if not found:
                child_list.append(node1)
        if row_0 < dimension:
            node2 = self.next_node(node, row_0, col_0, row_0 + 1, col_0, "down")
            found = search_equal_state(node2.state, list)
            if not found:
                child_list.append(node2)
        if col_0 > 0:
            node3 = self.next_node(node, row_0, col_0, row_0, col_0 - 1, "left")
            found = search_equal_state(node3.state, list)
            if not found:
                child_list.append(node3)
        if col_0 < dimension:
            node4 = self.next_node(node, row_0, col_0, row_0, col_0 + 1, "right")
            found = search_equal_state(node4.state, list)
            if not found:
                child_list.append(node4)

        child_list = ranking(child_list, goal_state)

        return list + child_list


class Node:
    root = None
    action = ""
    state = []
    path_cost = 1
    depth = 0
    ranking = 0 #the less the better

    def __init__(self, list, root, deep, action):
        self.root = root
        self.state = list
        self.depth = deep
        self.action = action


if __name__ == '__main__':

    agent = Agent()

    dimension = 3#int(input("digite a dimensao da matrix:"))

    #list = create_n_n_matrix(dimension)

    list = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    goal_state = list

    move = ["up", 'left', 'right', 'down']

    game_node = Node(list, None, 0, "")

    running_game = True
    print("Embaralhe a matrix utilizando os comandos abaixo:")
    while running_game:
        format_matrix(list)

        row_0, col_0 = find_number_row_and_col(list, 0)


        if row_0 != 0:
            print("1 - cima")
        if col_0 != 0:
            print("2 - esquerda")
        if col_0 < dimension - 1:
            print("3 - direita")
        if row_0 < dimension - 1:
            print("4 - baixo")

        print("5 - embaralhar")
        print("0 - sair")

        op = input("digite a opcao:")

        if op == '1':
            if row_0 == 0:
                continue
            game_node = agent.next_node(game_node, row_0, col_0, row_0 - 1, col_0, "up")
        elif op == '2':
            if col_0 == 0:
                continue
            game_node = agent.next_node(game_node, row_0, col_0, row_0, col_0 - 1, "left")
        elif op == '3':
            if col_0 == dimension - 1:
                continue
            game_node = agent.next_node(game_node, row_0, col_0, row_0, col_0 + 1, "right")
        elif op == '4':
            if row_0 == dimension - 1:
                continue
            game_node = agent.next_node(game_node, row_0, col_0, row_0 + 1, col_0, "down")
        elif op == '5':

            count = 0
            while count < 5:

                row_0, col_0 = find_number_row_and_col(game_node.state, 0)

                move_options = {
                    'left': [row_0, col_0 - 1],
                    'right': [row_0, col_0 + 1],
                    'up': [row_0 - 1, col_0],
                    'down': [row_0 + 1, col_0]
                }

                position = randint(0, 3)
                option_value = move[position]

                row = move_options[option_value][0]
                col = move_options[option_value][1]

                if row_0 == 0 and option_value == "up":
                    continue
                if col_0 == 0 and option_value == "left":
                    continue
                if col_0 == dimension - 1 and option_value == "right":
                    continue
                if row_0 == dimension - 1 and option_value == "down":
                    continue

                game_node = agent.next_node(game_node, row_0, col_0, row, col, option_value)
                count += 1
        else:
            running_game = False

        list = game_node.state

    node = Node(list, None, 0, "")

    node_list = []

    node_list.append(node)

    success = agent.goal(node.state, goal_state)

    count_process = 0

    msg = "sucesso"

    print("1 - largura  \n2 - profundidade\n")
    op = input("digite a opcao de busca:")

    if op == "1":
        search_type = 0
    if op == "2":
        search_type = -1

    if op != "2" and op != "1":
        print("erro")
        exit()

    while not success:
        # for node_i in node_list:
        #     print(node_i.state)

        node_list.pop(search_type)

        node_list = agent.next(node, node_list, dimension, goal_state)

        node = node_list[search_type]
        success = agent.goal(node.state, goal_state)

        count_process += 1

        # if count_process == 1000:
        #     success = True
        #     msg = "Deu ruim"

    print(msg)
    print("estado do pai")
    format_matrix(node.root.state)
    print("estado do filho(final)")
    format_matrix(node.state)
    print("direcao", node.action)
    print("profundidade", node.depth)
    print("tentativas", count_process)

