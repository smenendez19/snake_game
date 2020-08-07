import sys
import pygame
import random
import os
import time

# Largo, Alto
size_game = width, height = 500, 500
size_window = width_w, height_w = 700, 500
bloque = 25
speed = 10

# Imagenes
path_source = "source"
food_image = pygame.transform.scale(pygame.image.load(os.path.join(path_source,"cereza.png")),(bloque, bloque))
snake_head_image = pygame.transform.scale(pygame.image.load(os.path.join(path_source,"snake.png")),(bloque, bloque))

# Colores RGB
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

# Clases


class Snake():
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.body = [[self.x, self.y]]
        self.speed = speed
        self.color = green
        self.direction = "R"
        self.angle = -90

    def draw(self, screen):
        for b in self.body[:len(self.body) -1]:
            pygame.draw.rect(screen, self.color, [
                b[0], b[1], self.width, self.height])
        screen.blit(pygame.transform.rotate(snake_head_image,self.angle),(self.x,self.y))

    def set_direction(self, direction):
        self.direction = direction

    def set_angle(self, angle):
        self.angle = angle

    def add_body(self, x, y):
        self.body.append([x, y])


class Food():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.blit(food_image,(self.x,self.y))

    def set_x(self, width):
        self.x = round(random.randrange(0, width - bloque) / bloque) * bloque

    def set_y(self, height):
        self.y = round(random.randrange(0, height - bloque) / bloque) * bloque

# Funciones


def draw_window(width, rows, screen):
    # Fondo
    screen.fill(black)
    # Grilla de lineas (robado de alguna pagina)
    size_block = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + size_block
        y = y + size_block
        pygame.draw.line(screen, white, (x, 0), (x, width))
        pygame.draw.line(screen, white, (0, y), (width, y))

# Main

# Creacion de objetos, parametros del juego

pygame.init()
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size_window)

# Variables Booleanos

run_loop = True
run_game = False
start_game = False
pause = False

# Fuentes texto

font = pygame.font.Font('freesansbold.ttf', 20)
font_2 = pygame.font.Font('freesansbold.ttf', 12)

# Loop principal
while run_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
            run_loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                run_game = True
    if run_game:
        count_food = 0
        snake_head = Snake(250, 250, bloque, bloque, bloque)
        food_block = Food(round(random.randrange(0, width - bloque) / bloque) * bloque,
                round(random.randrange(0, height - bloque) / bloque) * bloque, bloque, bloque)
    
    # Loop del juego
    while run_game:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                run_loop = False
            if event.type == pygame.KEYDOWN:
                if not pause:
                    if event.key == pygame.K_LEFT and snake_head.direction not in ("R"):
                        snake_head.set_direction("L")
                        snake_head.set_angle(90)
                    elif event.key == pygame.K_RIGHT and snake_head.direction not in ("L"):
                        snake_head.set_direction("R")
                        snake_head.set_angle(-90)
                    elif event.key == pygame.K_UP and snake_head.direction not in ("D"):
                        snake_head.set_direction("U")
                        snake_head.set_angle(0)
                    elif event.key == pygame.K_DOWN and snake_head.direction not in ("U"):
                        snake_head.set_direction("D")
                        snake_head.set_angle(180)
                if event.key == pygame.K_SPACE:
                    pause = not pause

        # Valores viejos de x, y
        old_x = snake_head.x
        old_y = snake_head.y

        if not pause:
            if snake_head.direction == "U":
                snake_head.y -= snake_head.speed
            elif snake_head.direction == "D":
                snake_head.y += snake_head.speed
            elif snake_head.direction == "L":
                snake_head.x -= snake_head.speed
            elif snake_head.direction == "R":
                snake_head.x += snake_head.speed

            # Cuerpo de la snake_head
            snake_head.add_body(snake_head.x, snake_head.y)
            if len(snake_head.body) > count_food:
                del snake_head.body[0]
            
            # Colision con el cuerpo
            for body in snake_head.body[:len(snake_head.body) - 1]:
                if body[0] == snake_head.x and body[1] == snake_head.y:
                    run_game = False
                    break
            
            # Agarrar comida
            if snake_head.x == food_block.x and snake_head.y == food_block.y:
                count_food += 1
                food_block.set_x(width)
                food_block.set_y(height)
                snake_head.add_body(old_x, old_y)

            # Colision con los limites
            if snake_head.x > size_game[0] - snake_head.width or snake_head.x < 0 or snake_head.y > size_game[1] - snake_head.height or snake_head.y < 0:
                run_game = False
                break

        # Dibujo la ventana
        draw_window(width, width // bloque, screen)
        snake_head.draw(screen)
        food_block.draw(screen)

        # Texto / Puntaje
        if pause:
            text_pause = font.render('PAUSA', True, white, black)
            screen.blit(text_pause,(width_w - 150, 0))
        else:
            text_pause = font.render('', True, white, black)
            screen.blit(text_pause,(width_w - 150, 0))

        text_score = font_2.render(f"Score: {count_food}", True, white,black)
        screen.blit(text_score,(width_w - 180, 70))

        # Actualizar ventana
        pygame.display.update()

    draw_window(width, width // bloque, screen)
    if not run_game:
        text_start = font_2.render('Presiona S para comenzar', True,white,black)
        screen.blit(text_start,(width_w - 180, 50))
    else:
        text_start = font_2.render('', True,white,black)
        screen.blit(text_start,(width_w - 180, 50))

    # Actualizar ventana
    pygame.display.update()

pygame.quit()
