# Import modules
import os
import random
import sys

import pygame
import yaml

# AI
from ai.basic_algorithm import basic_ai
from ai.hamiltonian_cicle import hamiltonian_cicle

# Clases
from classes.Food import Food
from classes.Snake import Snake

# Environment Variables
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Variables PATH
SOURCE_PATH = os.path.join(os.path.dirname(sys.argv[0]), "source")
CONFIG_PATH = os.path.join(os.path.dirname(sys.argv[0]), "config")


# Clase principal SnakeGame
class SnakeGame:
    def __init__(self, ai_snake=False, ai_function=None, snake=None, config={}):
        # Comprobaciones
        if ai_snake and not ai_function:
            print("Error, necesita cargar una funcion de IA si va a utilizar una IA")
        if not snake:
            print("Error, necesita cargar un Snake")
            sys.exit(1)

        # Carga de la configuracion
        self.config = config

        # Variables de configuracion del juego
        self.width_game, self.height_game = self.config["sizes"]["game"]
        self.width_window, self.height_window = self.config["sizes"]["window"]
        self.block = self.config["sizes"]["block"]
        self.speed = self.config["game"]["speed"]
        self.run_loop = True
        self.run_game = False
        self.pause = False
        self.count_food = 0

        # Inicio del juego
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width_window, self.height_window))
        pygame.init()

        # Cargo las fuentes e imagenes
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.font_2 = pygame.font.Font("freesansbold.ttf", 12)
        self.food_image = pygame.transform.scale(
            pygame.image.load(os.path.join(SOURCE_PATH, "cereza.png")),
            (self.block, self.block),
        )
        pygame.display.set_caption("Snake Game")
        self.data_state = {"STATUS": "START"}

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
                self.data_state = {
                    "board_size": (self.width_game, self.height_game),
                    "block_size": self.block,
                    "snake_size": None,
                    "snake_body": [],
                    "food_count": 0,
                    "food_position": [],
                    "STATUS": "START",
                    "direction": None,
                }
                self.data_state = self.loop_game(snake, ai_function, self.speed, self.data_state)

            # Textos de la ventana
            self.draw_window(self.width_game, self.width_game // self.block, self.screen)
            if not self.run_game:
                text_start = self.font_2.render(
                    "Presiona R para comenzar",
                    True,
                    self.config["colors"]["white"],
                    self.config["colors"]["black"],
                )
                self.screen.blit(text_start, (self.width_window - 180, 50))
            else:
                text_start = self.font_2.render(
                    "",
                    True,
                    self.config["colors"]["white"],
                    self.config["colors"]["black"],
                )
                self.screen.blit(text_start, (self.width_window - 180, 50))
            text_title = self.font.render(
                "SNAKE GAME",
                True,
                self.config["colors"]["white"],
                self.config["colors"]["black"],
            )
            self.screen.blit(text_title, (self.width_window - 180, 10))
            text_score = self.font_2.render(
                f"Score: {self.count_food}",
                True,
                self.config["colors"]["white"],
                self.config["colors"]["black"],
            )
            self.screen.blit(text_score, (self.width_window - 180, 70))
            if self.data_state["STATUS"] == "GAMEOVER":
                text_game_over = self.font.render(
                    "GAME OVER",
                    True,
                    self.config["colors"]["white"],
                    self.config["colors"]["black"],
                )
                self.screen.blit(text_game_over, (self.width_game // 2 - 60, self.height_game // 2))
            elif self.data_state["STATUS"] == "WINNER":
                text_game_over = self.font.render(
                    "GANASTE",
                    True,
                    self.config["colors"]["white"],
                    self.config["colors"]["black"],
                )
                self.screen.blit(text_game_over, (self.width_game // 2 - 60, self.height_game // 2))

            # Actualizar ventana
            pygame.display.update()

        # Salir del juego
        pygame.quit()

    # Loop del juego
    def loop_game(self, snake, ai_function, speed, data_state={}):
        self.count_food = 0

        snake_player = snake
        snake_player.set_start_position(self.width_game // 2, self.height_game // 2)

        food_block = Food(
            round(random.randrange(0, self.width_game - self.block) / self.block) * self.block,
            round(random.randrange(0, self.height_game - self.block) / self.block) * self.block,
            self.block,
            self.block,
            self.food_image,
            self.block,
        )

        # Inicio del juego
        while self.run_game:
            self.clock.tick(speed)

            # Guardo en data_state los valores actuales (para la AI)
            data_state["snake_size"] = len(snake_player.body)
            data_state["snake_body"] = snake_player.body
            data_state["snake_head"] = snake_player.body[-1]
            data_state["snake_tail"] = snake_player.body[0]
            data_state["food_count"] = self.count_food
            data_state["food_position"] = [(food_block.x, food_block.y)]
            data_state["STATUS"] = "PLAYING"
            data_state["direction"] = snake_player.direction

            print(data_state)

            # Eventos de teclado o IA
            if ai_function is None:
                key = self.get_events()
                if key == "QUIT":
                    self.run_game = False
                    self.run_loop = False
                if key == "SPACE":
                    self.pause = not self.pause
                if not self.pause and key is not None:
                    snake_player.move_snake(key)
            else:
                key = self.get_events()
                if key == "QUIT":
                    self.run_game = False
                    self.run_loop = False
                if key == "SPACE":
                    self.pause = not self.pause
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run_game = False
                        self.run_loop = False
                if not self.pause:
                    predicted_move = ai_function(data_state)
                    snake_player.move_snake(predicted_move)

            if not self.pause:
                # Colision con el cuerpo
                for body in snake_player.body[: len(snake_player.body) - 1]:
                    if body[0] == snake_player.x and body[1] == snake_player.y:
                        self.run_game = False
                        data_state["STATUS"] = "GAMEOVER"
                        break

                # Cuerpo de la snake_player
                snake_player.add_body(snake_player.x, snake_player.y)

                # Agarrar comida
                if snake_player.x == food_block.x and snake_player.y == food_block.y:
                    self.count_food += 1
                    possible_placemments = food_block.possible_placements(snake_player.body, self.width_game, self.height_game)
                    if len(possible_placemments) > 0:
                        food_block.set_food_position(snake_player.body, self.width_game, self.height_game)
                    else:
                        self.run_game = False
                        data_state["STATUS"] = "WINNER"
                        break
                else:
                    snake_player.remove_tail()

                # Colision con los limites
                if (
                    snake_player.x > self.width_game - snake_player.width
                    or snake_player.x < 0
                    or snake_player.y > self.height_game - snake_player.height
                    or snake_player.y < 0
                ):
                    self.run_game = False
                    data_state["STATUS"] = "GAMEOVER"
                    break

            # Dibujo la ventana
            self.draw_window(self.width_game, self.width_game // self.block, self.screen)
            snake_player.draw(self.screen)
            food_block.draw(self.screen)

            # Texto / Puntaje dentro del juego
            if self.pause:
                text_pause = self.font.render(
                    "PAUSA",
                    True,
                    self.config["colors"]["white"],
                    self.config["colors"]["black"],
                )
                self.screen.blit(text_pause, (self.width_game // 2 - 20, self.height_game // 2))
            else:
                text_pause = self.font.render(
                    "",
                    True,
                    self.config["colors"]["white"],
                    self.config["colors"]["black"],
                )
                self.screen.blit(text_pause, (self.width_game // 2 - 20, self.height_game // 2))

            text_title = self.font.render(
                "SNAKE GAME",
                True,
                self.config["colors"]["white"],
                self.config["colors"]["black"],
            )
            self.screen.blit(text_title, (self.width_window - 180, 10))
            text_score = self.font_2.render(
                f"Score: {self.count_food}",
                True,
                self.config["colors"]["white"],
                self.config["colors"]["black"],
            )
            self.screen.blit(text_score, (self.width_window - 180, 70))

            # Actualizar ventana
            pygame.display.update()
        return data_state

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
        screen.fill(self.config["colors"]["black"])
        # Grilla de lineas (robado de alguna pagina)
        size_block = width // rows
        x = 0
        y = 0
        for _ in range(rows):
            x = x + size_block
            y = y + size_block
            pygame.draw.line(screen, self.config["colors"]["white"], (x, 0), (x, width))
            pygame.draw.line(screen, self.config["colors"]["white"], (0, y), (width, y))


# Main
if __name__ == "__main__":
    # Carga del archivo de configuracion
    config = yaml.load(open(os.path.join(CONFIG_PATH, "config_snake.yaml")), Loader=yaml.FullLoader)
    block = config["sizes"]["block"]
    snake_player_image = pygame.transform.scale(pygame.image.load(os.path.join(SOURCE_PATH, "snake.png")), (block, block))
    snake = Snake(
        width=block,
        height=block,
        speed=block,
        body_color=config["colors"][config["snake"]["body_color"]],
        head_image=snake_player_image,
        tail_color=config["colors"][config["snake"]["tail_color"]],
    )
    ai_snake = config["ai"]["enable"]
    if ai_snake:
        ai_module = __import__(config["ai"]["package"], fromlist=[config["ai"]["function"]])
        ai_function = getattr(ai_module, config["ai"]["function"])
        SnakeGame(ai_snake=ai_snake, ai_function=ai_function, config=config, snake=snake)
    else:
        SnakeGame(ai_snake=ai_snake, config=config, snake=snake)
