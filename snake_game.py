import time
import sys
import os
import random

# Environment Variables
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

# Clases

class SnakeGame:
    def __init__(self, ai_snake=False):
        self.ai_snake = ai_snake
        # Colores RGB
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        self.red = 255, 0, 0
        self.green = 0, 255, 0
        self.blue = 0, 0, 255
        # Largo, Alto
        self.width_game, self.height_game = 500, 500
        self.width_window, self.height_window = 700, 500
        self.block = 25
        self.speed = 100
        # Inicio las variables principales
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width_window, self.height_window))
        self.run_loop = True
        self.run_game = False
        self.pause = False
        self.count_food = 0
        # Inicio del juego
        pygame.init()
        # Cargo las fuentes e imagenes
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.font_2 = pygame.font.Font('freesansbold.ttf', 12)
        path_source = "source"
        self.food_image = pygame.transform.scale(pygame.image.load(os.path.join(path_source,"cereza.png")),(self.block, self.block))
        self.snake_player_image = pygame.transform.scale(pygame.image.load(os.path.join(path_source,"snake.png")),(self.block, self.block))
        pygame.display.set_caption('Snake Game')
        self.data_state = {
        }

        # Loop principal 
        while self.run_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False
                    self.run_loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.run_game = True

            # Iniciar juego
            if self.run_game:
                self.loop_game()

            # Textos de la ventana
            self.draw_window(self.width_game, self.width_game // self.block, self.screen)
            if not self.run_game:
                text_start = self.font_2.render('Presiona R para comenzar', True,self.white, self.black)
                self.screen.blit(text_start,(self.width_window - 180, 50))
            else:
                text_start = self.font_2.render('', True,self.white, self.black)
                self.screen.blit(text_start,(self.width_window - 180, 50))
            
            text_title = self.font.render('SNAKE GAME', True, self.white, self.black)
            self.screen.blit(text_title,(self.width_window - 180, 10))
            text_score = self.font_2.render(f"Score: {self.count_food}", True, self.white, self.black)
            self.screen.blit(text_score,(self.width_window - 180, 70))
            text_game_over = self.font.render('GAME OVER', True, self.white, self.black)
            self.screen.blit(text_game_over,(self.width_game // 2 - 60, self.height_game // 2))
            # Actualizar ventana
            pygame.display.update()

        # Salir del juego
        pygame.quit()


    # Loop del juego
    def loop_game(self):
        self.count_food = 0
        self.data_state = {
            "board_size": (self.width_game, self.height_game),
            "snake_size" : None,
            "snake_body" : [],
            "food_count" : 0,
            "food_position" : [],
            "status" : "STARTING",
            "direction" : None
        }
        snake_player = Snake(250, 250, self.block, self.block, self.block, self.green, self.snake_player_image)
        food_block = Food(round(random.randrange(0, self.width_game - self.block) / self.block) * self.block, round(random.randrange(0, self.height_game - self.block) / self.block) * self.block, self.block, self.block, self.food_image, self.block)
        while self.run_game:
            self.clock.tick(self.speed)
            
            # Guardo en data_state los valores actuales (para la AI)
            self.data_state["snake_size"] = len(snake_player.body)
            self.data_state["snake_body"] = snake_player.body
            self.data_state["food_count"] = self.count_food
            self.data_state["food_position"] = [(food_block.x, food_block.y)]
            self.data_state["status"] = "PLAYING"
            self.data_state["direction"] = snake_player.direction

            # Eventos
            if not self.ai_snake:
                key = self.get_events()
                if key == "QUIT":
                    self.run_game = False
                    self.run_loop = False
                if key == "SPACE":
                    self.pause = not self.pause
                if not self.pause and key is not None:
                    snake_player.move_snake(key)
            elif self.ai_snake:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run_game = False
                        self.run_loop = False
                predicted_move = self.predict_move(self.data_state)
                key = None
                if predicted_move == "UP":
                    key = "U"
                elif predicted_move == "DOWN":
                    key = "D"
                elif predicted_move == "LEFT":
                    key = "L"
                elif predicted_move == "RIGHT":
                    key = "R"
                snake_player.move_snake(key)

            # Valores viejos de x, y
            old_x, old_y = snake_player.get_tail()

            if not self.pause:
                if snake_player.direction == "U":
                    snake_player.y -= snake_player.speed
                elif snake_player.direction == "D":
                    snake_player.y += snake_player.speed
                elif snake_player.direction == "L":
                    snake_player.x -= snake_player.speed
                elif snake_player.direction == "R":
                    snake_player.x += snake_player.speed
                
                # Colision con el cuerpo
                for body in snake_player.body[:len(snake_player.body) - 1]:
                    if body[0] == snake_player.x and body[1] == snake_player.y:
                        self.run_game = False
                        self.data_state["STATUS"] = "GAME OVER"
                        break
                
                # Agarrar comida
                if snake_player.x == food_block.x and snake_player.y == food_block.y:
                    self.count_food += 1
                    food_block.set_x(self.width_game)
                    food_block.set_y(self.height_game)
                    snake_player.add_body(old_x, old_y)

                # Cuerpo de la snake_player
                snake_player.add_body(snake_player.x, snake_player.y)
                if len(snake_player.body) > self.count_food:
                    del snake_player.body[0]

                # Colision con los limites
                if snake_player.x > self.width_game - snake_player.width or snake_player.x < 0 or snake_player.y > self.height_game - snake_player.height or snake_player.y < 0:
                    self.run_game = False
                    self.data_state["STATUS"] = "GAME OVER"
                    break

            # Dibujo la ventana
            self.draw_window(self.width_game, self.width_game // self.block, self.screen)
            snake_player.draw(self.screen)
            food_block.draw(self.screen)

            # Texto / Puntaje dentro del juego
            if self.pause:
                text_pause = self.font.render('PAUSA', True, self.white, self.black)
                self.screen.blit(text_pause,(self.width_game // 2 - 20, self.height_game // 2))
            else:
                text_pause = self.font.render('', True, self.white, self.black)
                self.screen.blit(text_pause,(self.width_game // 2 - 20, self.height_game // 2))

            text_title = self.font.render('SNAKE GAME', True, self.white, self.black)
            self.screen.blit(text_title,(self.width_window - 180, 10))
            text_score = self.font_2.render(f"Score: {self.count_food}", True, self.white, self.black)
            self.screen.blit(text_score,(self.width_window - 180, 70))
            # Actualizar ventana
            pygame.display.update()

    # Algoritmo de AI (basico)
    def predict_move(self, data):
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
            if my_head[0] == board_height - self.block:
                possible_moves.remove("RIGHT")
            if my_head[0] == 0:
                possible_moves.remove("LEFT")
            if my_head[1] == 0:
                possible_moves.remove("UP")
            if my_head[1] == board_width - self.block:
                possible_moves.remove("DOWN")
            return possible_moves

        def priorize_food(data, my_head):
            distance_food = {
                "UP" : None,
                "DOWN" : None,
                "LEFT" : None,
                "RIGHT" : None
            }
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
            my_body_parts = my_body[:len(my_body) - 1]
            for body_parts in my_body_parts:
                if  body_parts[0] == my_head[0] - self.block and body_parts[1] == my_head[1]:
                    if "LEFT" in possible_moves:
                        possible_moves.remove("LEFT")
                if  body_parts[0] == my_head[0] + self.block and body_parts[1] == my_head[1]:
                    if "RIGHT" in possible_moves:
                        possible_moves.remove("RIGHT")
                if  body_parts[0] == my_head[0] and body_parts[1] == my_head[1] + self.block:
                    if "DOWN" in possible_moves:
                        possible_moves.remove("DOWN")
                if  body_parts[0] == my_head[0] and body_parts[1] == my_head[1] - self.block:
                    if "UP" in possible_moves:
                        possible_moves.remove("UP")
            return possible_moves

        def choose_move(data):
            my_head = data["snake_body"][-1]  
            my_body = data["snake_body"] 
            possible_moves = ["UP", "LEFT", "RIGHT", "DOWN"]
            # Evitar chocar con el cuello
            possible_moves = avoid_my_neck(data, possible_moves)

            board_height = data["board_size"][0]
            board_width = data["board_size"][1]

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
            
            #print(possible_moves, move, data["snake_body"])
            return move
        return choose_move(data)

    # Toma de eventos de teclado
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if not self.pause:
                    if event.key == pygame.K_LEFT:
                        return "L"
                    elif event.key == pygame.K_RIGHT:
                        return "R"
                    elif event.key == pygame.K_UP:
                        return "U"
                    elif event.key == pygame.K_DOWN:
                        return "D"
                if event.key == pygame.K_SPACE:
                    return "SPACE"

    # Dibujo el tablero
    def draw_window(self, width, rows, screen):
        # Fondo
        screen.fill(self.black)
        # Grilla de lineas (robado de alguna pagina)
        size_block = width // rows
        x = 0
        y = 0
        for l in range(rows):
            x = x + size_block
            y = y + size_block
            pygame.draw.line(screen, self.white, (x, 0), (x, width))
            pygame.draw.line(screen, self.white, (0, y), (width, y))

class Snake:
    def __init__(self, x, y, width, height, speed, color, head_image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.body = [[self.x, self.y]]
        self.speed = speed
        self.color = color
        self.direction = "R"
        self.angle = -90
        self.head_image = head_image

    def draw(self, screen):
        for x, y  in self.body:
            pygame.draw.rect(screen, self.color, [x, y, self.width, self.height])
        screen.blit(pygame.transform.rotate(self.head_image, self.angle),(self.x, self.y))

    def set_direction(self, direction):
        self.direction = direction

    def set_angle(self, angle):
        self.angle = angle

    def add_body(self, x, y):
        self.body.append([x, y])

    def get_direction(self):
        return self.direction
    
    def get_tail(self):
        return self.body[len(self.body)-1]

    # Movimiento del snake
    def move_snake(self, key):
        angle_dicc = {
            "R": -90,
            "L": 90,
            "U": 0,
            "D": 180
        }
        opposite_dicc = {
            "R": "L",
            "L": "R",
            "U": "D",
            "D": "U"
        }
        if key in ("R", "L", "U", "D"):
            if opposite_dicc[key] != self.get_direction():
                self.set_direction(key)
                self.set_angle(angle_dicc[key])


class Food:
    def __init__(self, x, y, width, height, food_image, block_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block_size = block_size
        self.food_image = food_image

    def draw(self, screen):
        screen.blit(self.food_image, (self.x, self.y))

    def set_x(self, width):
        self.x = round(random.randrange(0, width - self.block_size) / self.block_size) * self.block_size

    def set_y(self, height):
        self.y = round(random.randrange(0, height - self.block_size) / self.block_size) * self.block_size

# Funciones

# Main
if __name__ == "__main__":
    SnakeGame(ai_snake=True)