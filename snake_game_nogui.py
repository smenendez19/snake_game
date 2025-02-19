# Import modules
import random

import pygame

# AI
from ai.basic_algorithm import basic_ai
from ai.hamiltonian_cicle import hamiltonian_cicle

# Clases
from classes.Food import Food
from classes.Snake import Snake


class SnakeGame:
    def __init__(self, ai_snake=False, ai_function=None, snake=None, config={}):

        # Init conditions
        if ai_snake and not ai_function:
            raise Exception("Error, necesita cargar una funcion de IA")
        if not snake:
            raise Exception("Error, necesita cargar una serpiente")

        # Load config
        self.config = config

        # Init variables
        self.width_game, self.height_game = self.config["sizes"]["game"]
        self.block = self.config["sizes"]["block"]
        self.speed = self.config["game"]["speed"]
        self.run_game = False
        self.count_food = 0
        self.time_left = 100
        self.ai_function = ai_function
        self.snake = snake
        self.curr_step = 0
        self.clock = pygame.time.Clock()
        self.data_state = {}
        self.data_state["status"] = "GAMEOVER"

    # Start
    def start(self):
        self.run_game = True

        self.snake.set_start_position(self.width_game // 2, self.height_game // 2)

        food_block = Food(
            round(random.randrange(0, self.width_game - self.block) / self.block)
            * self.block,
            round(random.randrange(0, self.height_game - self.block) / self.block)
            * self.block,
            self.block,
            self.block,
            None,
            self.block,
        )

        food_block.set_food_position(
            self.snake.body, self.width_game, self.height_game
        )

        self.data_state = {
            "board_size": (self.width_game, self.height_game),
            "block_size": self.block,
            "snake_size": len(self.snake.body),
            "snake_body": self.snake.body,
            "snake_head": self.snake.body[-1],
            "snake_tail": self.snake.body[0],
            "food_count": self.count_food,
            "food_position": [(food_block.x, food_block.y)],
            "status": "START",
            "step": self.curr_step,
            "direction": self.snake.get_direction(),
            "move": None,
        }

        return self.data_state

    # Check game running
    def is_running(self):
        return self.run_game

    # Step
    def step(self):

        # Game not started
        if not self.run_game:
            return self.data_state

        self.data_state["status"] = "PLAYING"

        food_block = Food(
            round(random.randrange(0, self.width_game - self.block) / self.block)
            * self.block,
            round(random.randrange(0, self.height_game - self.block) / self.block)
            * self.block,
            self.block,
            self.block,
            None,
            self.block,
        )

        # Movement events
        predicted_move = self.ai_function(self.data_state)
        self.snake.move_snake(predicted_move)

        self.data_state["move"] = predicted_move

        # Body collide
        for body in self.snake.body[: len(self.snake.body) - 1]:
            if body[0] == self.snake.x and body[1] == self.snake.y:
                self.run_game = False
                self.data_state["STATUS"] = "GAMEOVER"
                break

        # Time left
        if self.time_left <= 0:
            self.run_game = False
            self.data_state["status"] = "GAMEOVER"

        # Add body
        self.snake.add_body(self.snake.x, self.snake.y)

        # Get food
        if self.snake.x == self.snake.x and self.snake.y == self.snake.y:
            self.count_food += 1
            possible_placemments = food_block.possible_placements(
                self.snake.body, self.width_game, self.height_game
            )
            if len(possible_placemments) > 0:
                food_block.set_food_position(
                    self.snake.body, self.width_game, self.height_game
                )
            else:
                self.run_game = False
                self.data_state["status"] = "WINNER"

            self.time_left = 100
        else:
            self.snake.remove_tail()
            self.time_left -= 1

        # Limit collide
        if (
            self.snake.x > self.width_game - self.snake.width
            or self.snake.x < 0
            or self.snake.y > self.height_game - self.snake.height
            or self.snake.y < 0
        ):
            self.run_game = False
            self.data_state["status"] = "GAMEOVER"

        self.curr_step += 1

        # Data State
        self.data_state["snake_size"] = len(self.snake.body)
        self.data_state["snake_body"] = self.snake.body
        self.data_state["snake_head"] = self.snake.body[-1]
        self.data_state["snake_tail"] = self.snake.body[0]
        self.data_state["food_count"] = self.count_food
        self.data_state["food_position"] = []
        self.data_state["direction"] = self.snake.direction
        self.data_state["time_left"] = self.time_left
        self.data_state["step"] = self.curr_step

        return self.data_state

    # Game Loop
    def loop_game(self, ai_function, speed, data_state={}):
        snake_player = self.snake
        snake_player.set_start_position(self.width_game // 2, self.height_game // 2)

        food_block = Food(
            round(random.randrange(0, self.width_game - self.block) / self.block)
            * self.block,
            round(random.randrange(0, self.height_game - self.block) / self.block)
            * self.block,
            self.block,
            self.block,
            None,
            self.block,
        )

        # Run game
        while self.run_game:
            self.clock.tick(speed)

            # Data State
            data_state["snake_size"] = len(snake_player.body)
            data_state["snake_body"] = snake_player.body
            data_state["snake_head"] = snake_player.body[-1]
            data_state["snake_tail"] = snake_player.body[0]
            data_state["food_count"] = self.count_food
            data_state["food_position"] = [(food_block.x, food_block.y)]
            data_state["status"] = "PLAYING"
            data_state["direction"] = snake_player.direction
            data_state["time_left"] = self.time_left

            # Movement events
            predicted_move = ai_function(data_state)
            snake_player.move_snake(predicted_move)

            data_state["move"] = predicted_move

            print(data_state)

            # Body collide
            for body in snake_player.body[: len(snake_player.body) - 1]:
                if body[0] == snake_player.x and body[1] == snake_player.y:
                    self.run_game = False
                    data_state["STATUS"] = "GAMEOVER"
                    break

            # Time left
            if self.time_left <= 0:
                self.run_game = False
                data_state["status"] = "GAMEOVER"
                break

            # Add body
            snake_player.add_body(snake_player.x, snake_player.y)

            # Get food
            if snake_player.x == food_block.x and snake_player.y == food_block.y:
                self.count_food += 1
                possible_placemments = food_block.possible_placements(
                    snake_player.body, self.width_game, self.height_game
                )
                if len(possible_placemments) > 0:
                    food_block.set_food_position(
                        snake_player.body, self.width_game, self.height_game
                    )
                else:
                    self.run_game = False
                    data_state["status"] = "WINNER"
                    break
                self.time_left = 100
            else:
                snake_player.remove_tail()
                self.time_left -= 1

            # Limit collide
            if (
                snake_player.x > self.width_game - snake_player.width
                or snake_player.x < 0
                or snake_player.y > self.height_game - snake_player.height
                or snake_player.y < 0
            ):
                self.run_game = False
                data_state["status"] = "GAMEOVER"
                break

        return data_state


# Main
if __name__ == "__main__":
    snake = Snake(
        width=50,
        height=50,
        speed=50,
        body_color=None,
        head_image=None,
        tail_color=None,
    )

    snake_game = SnakeGame(
        ai_snake=True,
        ai_function=hamiltonian_cicle,
        config={"sizes": {"block": 50, "game": [500, 500]}, "game": {"speed": 1000}},
        snake=snake,
    )

    data = snake_game.start()

    print(data)

    while snake_game.is_running():
        data = snake_game.step()
        print(data)
