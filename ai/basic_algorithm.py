# Modules

import random


# Algoritmo de AI (basico)
def basic_ai(data):
    def avoid_my_neck(data, possible_moves):
        dir = data["direction"]
        if dir == "R":
            possible_moves.remove("LEFT")
        elif dir == "L":
            possible_moves.remove("RIGHT")
        elif dir == "U":
            possible_moves.remove("DOWN")
        elif dir == "D":
            possible_moves.remove("UP")
        return possible_moves

    def avoid_walls(board_height, board_width, my_head, possible_moves):
        if my_head[0] == board_height - data["block_size"]:
            possible_moves.remove("RIGHT")
        if my_head[0] == 0:
            possible_moves.remove("LEFT")
        if my_head[1] == 0:
            possible_moves.remove("UP")
        if my_head[1] == board_width - data["block_size"]:
            possible_moves.remove("DOWN")
        return possible_moves

    def priorize_food(data, my_head):
        distance_food = {"UP": None, "DOWN": None, "LEFT": None, "RIGHT": None}
        for food_pos in data["food_position"]:
            if my_head[0] < food_pos[0] and my_head[1] == food_pos[1]:
                if distance_food["RIGHT"] is None or distance_food["RIGHT"] > food_pos[0] - my_head[0]:
                    distance_food["RIGHT"] = food_pos[0] - my_head[0]
            elif my_head[0] > food_pos[0] and my_head[1] == food_pos[1]:
                if distance_food["LEFT"] is None or distance_food["LEFT"] > food_pos[0] + my_head[0]:
                    distance_food["LEFT"] = food_pos[0] + my_head[0]
            elif my_head[1] < food_pos[1] and my_head[0] == food_pos[0]:
                if distance_food["DOWN"] is None or distance_food["DOWN"] > food_pos[1] - my_head[1]:
                    distance_food["DOWN"] = food_pos[1] - my_head[1]
            elif my_head[1] > food_pos[1] and my_head[0] == food_pos[0]:
                if distance_food["UP"] is None or distance_food["UP"] > food_pos[1] - my_head[1]:
                    distance_food["UP"] = food_pos[1] + my_head[1]
        food_move = None
        min_dist = None
        for dir in distance_food:
            if distance_food[dir] is not None and (min_dist is None or distance_food[dir] < min_dist):
                min_dist = distance_food[dir]
                food_move = dir
        return food_move

    def avoid_body(my_head, my_body, possible_moves):
        if len(my_body) < 3:
            return possible_moves
        my_body_parts = my_body[: len(my_body) - 1]
        for body_parts in my_body_parts:
            if body_parts[0] == my_head[0] - data["block_size"] and body_parts[1] == my_head[1]:
                if "LEFT" in possible_moves:
                    possible_moves.remove("LEFT")
            if body_parts[0] == my_head[0] + data["block_size"] and body_parts[1] == my_head[1]:
                if "RIGHT" in possible_moves:
                    possible_moves.remove("RIGHT")
            if body_parts[0] == my_head[0] and body_parts[1] == my_head[1] + data["block_size"]:
                if "DOWN" in possible_moves:
                    possible_moves.remove("DOWN")
            if body_parts[0] == my_head[0] and body_parts[1] == my_head[1] - data["block_size"]:
                if "UP" in possible_moves:
                    possible_moves.remove("UP")
        return possible_moves

    def choose_move(data):
        my_head = data["snake_body"][-1]
        my_body = data["snake_body"]
        possible_moves = ["UP", "LEFT", "RIGHT", "DOWN"]
        board_height = data["board_size"][0]
        board_width = data["board_size"][1]

        # Evitar chocar con el cuello
        possible_moves = avoid_my_neck(data, possible_moves)

        # Evitar los bordes
        possible_moves = avoid_walls(board_height, board_width, my_head, possible_moves)

        # Evitar chocar con tu propio cuerpo
        possible_moves = avoid_body(my_head, my_body, possible_moves)

        # Tomar la ultima direccion en la que estuvo el snake segun el cuerpo
        if data["direction"] == "R":
            last_move = "RIGHT"
        elif data["direction"] == "L":
            last_move = "LEFT"
        elif data["direction"] == "U":
            last_move = "UP"
        elif data["direction"] == "D":
            last_move = "DOWN"

        # Priorizar movimiento hacia la comida mas cercana
        food_move = priorize_food(data, my_head)

        # Si no hay movimientos posibles volver a incluir la lista
        if len(possible_moves) == 0:
            possible_moves = ["UP", "LEFT", "RIGHT", "DOWN"]

        if food_move in possible_moves:
            move = food_move
        elif last_move in possible_moves:
            move = last_move
        else:
            move = random.choice(possible_moves)

        initial_move_letter = {
            "UP": "U",
            "DOWN": "D",
            "LEFT": "L",
            "RIGHT": "R",
        }

        return initial_move_letter[move]

    return choose_move(data)
