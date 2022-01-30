import pygame

class Snake:
    def __init__(self, x=0, y=0, width=0, height=0, speed=0, body_color=(0, 0, 0), head_image=None, tail_color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.body = []
        self.body_color = body_color
        self.tail_color = tail_color
        self.direction = "R"
        self.angle = -90
        self.head_image = head_image

    def draw(self, screen):
        for x, y in self.body:
            pygame.draw.rect(screen, self.body_color, [x, y, self.width, self.height])
            # Bordeado
            pygame.draw.rect(screen, (0, 0, 0), [x, y, self.width, self.height], width=1)
        # Color for tail
        pygame.draw.rect(screen, self.tail_color, [self.body[0][0], self.body[0][1], self.width, self.height])
        screen.blit(pygame.transform.rotate(self.head_image, self.angle),(self.x, self.y))

    def set_direction(self, direction):
        self.direction = direction

    def set_angle(self, angle):
        self.angle = angle

    def set_start_position(self, x, y):
        self.x = x
        self.y = y
        self.body = [[self.x, self.y]]

    def add_body(self, x, y):
        self.body.append([x, y])

    def get_direction(self):
        return self.direction
    
    def get_tail(self):
        return self.body[0]
    
    def remove_tail(self):
        del self.body[0]

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
        if key == "U":
            self.y -= self.speed
        elif key == "D":
            self.y += self.speed
        elif key == "L":
            self.x -= self.speed
        elif key == "R":
            self.x += self.speed