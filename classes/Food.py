import random


class Food:
    def __init__(self, x, y, width, height, food_image, block_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block_size = block_size
        self.food_image = food_image

    def possible_placements(self, body, width, height):
        possible_placemments = []
        for x in range(0, width, self.block_size):
            for y in range(0, height, self.block_size):
                if [x, y] not in body:
                    possible_placemments.append([x, y])
        return possible_placemments

    def set_food_position(self, body, width, height):
        possible_placemments = self.possible_placements(body, width, height)
        self.x, self.y = random.choice(possible_placemments)

    def draw(self, screen):
        screen.blit(self.food_image, (self.x, self.y))

    def set_x(self, width):
        self.x = round(random.randrange(0, width - self.block_size) / self.block_size) * self.block_size

    def set_y(self, height):
        self.y = round(random.randrange(0, height - self.block_size) / self.block_size) * self.block_size
