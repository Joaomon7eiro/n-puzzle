import copy
from random import randint
#from numpy import *


def find_row0_col0(list):
    row_0, col_0 = 0, 0
    for index_row, row in enumerate(list):
        for index_col, value in enumerate(row):
            if value == 0:
                row_0, col_0 = index_row, index_col
                break

    return row_0, col_0

def create_n_n_matrix(dimension):

    x = range(1, dimension*dimension + 1)

    x = reshape(x, (dimension, dimension))
    x[-1][-1] = 0

    return x


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

    def goal(self, node, dimension):
        dimension *= dimension
        count = 1
        for index_row in node.state:
            for index_col in index_row:
                if index_col != count:
                    if count == dimension:
                        return True
                    else:
                        return False
                else:
                    count += 1

    def next(self, node, list, dimension):

        dimension = dimension - 1

        row_0, col_0 = find_row0_col0(node.state)

        if row_0 > 0:
            node1 = self.next_node(node, row_0, col_0, row_0 - 1, col_0, "up")
            list.append(node1)
        if row_0 < dimension:
            node2 = self.next_node(node, row_0, col_0, row_0 + 1, col_0, "down")
            list.append(node2)
        if col_0 > 0:
            node3 = self.next_node(node, row_0, col_0, row_0, col_0 - 1, "left")
            list.append(node3)
        if col_0 < dimension:
            node4 = self.next_node(node, row_0, col_0, row_0, col_0 + 1, "right")
            list.append(node4)

        return list


class Node:
    root = None
    action = ""
    state = []
    path_cost = 1
    depth = 0

    def __init__(self, list, root, deep, action):
        self.root = root
        self.state = list
        self.depth = deep
        self.action = action


if __name__ == '__main__':

    agent = Agent()

    dimension = int(input("digite a dimensao da matrix:"))

    #list = create_n_n_matrix(dimension)

    list = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    move = ["cima", 'esquerda', 'direita', 'baixo']

    game_node = Node(list, None, 0, "")

    running_game = True
    print("Embaralhe a matrix utilizando os comandos abaixo:")
    while running_game:
        format_matrix(list)

        row_0, col_0 = find_row0_col0(list)

        if row_0 != 0:
            print("1 - cima")
        if col_0 != 0:
            print("2 - esquerda")
        if col_0 < dimension - 1:
            print("3 - direita")
        if row_0 < dimension - 1:
            print("4 - baixo")

        print("5 - embaralhar")

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

                row_0, col_0 = find_row0_col0(list)

                move_options = {
                    'esquerda': [row_0, col_0 - 1],
                    'direita': [row_0, col_0 + 1],
                    'cima': [row_0 - 1, col_0],
                    'baixo': [row_0 + 1, col_0]
                }

                positon = randint(0, 3)
                option_value = move[positon]

                row = move_options[option_value][0]
                col = move_options[option_value][1]

                if row_0 == 0 and option_value == "cima":
                    continue
                if col_0 == 0 and option_value == "esquerda":
                    continue
                if col_0 == dimension - 1 and option_value == "direita":
                    continue
                if row_0 == dimension - 1 and option_value == "baixo":
                    continue

                game_node = agent.next_node(game_node, row_0, col_0, row, col, "asd")

                list = game_node.state
                count += 1

        else:
            running_game = False

        list = game_node.state

    node = Node(list, None, 0, "")

    node_list = []

    node_list.append(node)

    success = agent.goal(node, dimension)

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

        node_list = agent.next(node, node_list, dimension)

        node = node_list[search_type]
        success = agent.goal(node, dimension)

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

