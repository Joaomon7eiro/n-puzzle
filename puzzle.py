from random import randint
from node import Node
from agent import Agent
from functions import format_matrix, find_number_row_and_col, next_node, create_n_n_matrix

if __name__ == '__main__':

    agent = Agent()

    dimension = int(input("digite a dimensao da matrix:"))

    list = create_n_n_matrix(dimension)

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
            game_node = next_node(game_node, row_0, col_0, row_0 - 1, col_0, "up")
        elif op == '2':
            if col_0 == 0:
                continue
            game_node = next_node(game_node, row_0, col_0, row_0, col_0 - 1, "left")
        elif op == '3':
            if col_0 == dimension - 1:
                continue
            game_node = next_node(game_node, row_0, col_0, row_0, col_0 + 1, "right")
        elif op == '4':
            if row_0 == dimension - 1:
                continue
            game_node = next_node(game_node, row_0, col_0, row_0 + 1, col_0, "down")
        elif op == '5':

            count = 0
            while count < 100:

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

                game_node = next_node(game_node, row_0, col_0, row, col, option_value)
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
        for node_i in node_list:
            print(node_i.action)

        node_list.pop(search_type)

        node_list = agent.next(node, node_list, dimension, goal_state)

        node = node_list[search_type]
        success = agent.goal(node.state, goal_state)

        count_process += 1


    print(msg)
    print("estado do pai")
    format_matrix(node.root.state)
    print("estado do filho(final)")
    format_matrix(node.state)
    print("direcao", node.action)
    print("profundidade", node.depth)
    print("tentativas", count_process)

