import random
import numpy as np
import snake_sense

class Game:
    def __init__(self):
        self.reaction = [0, 1, 0, 0]
        self.isAlive = True
        self.move_without_food = 0
        self.head_position = [2, 2]
        self.body_positions = [[2, 2]]
        self.head_direction = 'right'
        self.food_position = [5, 5]
        self.fitness_score = 0
        self.level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def move_snake_head(self):
        if self.head_direction == 'up':
            self.head_position[0] -= 1
        if self.head_direction == 'down':
            self.head_position[0] += 1
        if self.head_direction == 'left':
            self.head_position[1] -= 1
        if self.head_direction == 'right':
            self.head_position[1] += 1

    def snake_move_and_grow(self):
        self.body_positions.append(self.head_position.copy())
        self.level[self.head_position[0]][self.head_position[1]] = 1

    def snake_move(self):
        self.body_positions.append(self.head_position.copy())
        self.level[self.head_position[0]][self.head_position[1]] = 1
        self.level[self.body_positions[0][0]][self.body_positions[0][1]] = 0
        self.body_positions.pop(0)

    def possible_move(self):
        if (self.head_position[0] < 0 or
            self.head_position[1] < 0 or
            self.head_position[0] > 9 or
                self.head_position[1] > 9):
            return False
        if self.level[self.head_position[0]][self.head_position[1]] == 1:
            return False

    def there_is_food(self):
        if self.level[self.head_position[0]][self.head_position[1]] == 2:
            return True

    def new_food(self):
        self.level[self.food_position[0]][self.food_position[1]] = 1
        self.food_pos = [random.randint(0, 9), random.randint(0, 9)]
        while (self.level[self.food_position[0]][self.food_position[1]] != 0):
            self.food_position = [random.randint(0, 9), random.randint(0, 9)]
        self.level[self.food_position[0]][self.food_position[1]] = 2
        
    def gameplay(self,net):

        while self.isAlive:
            if self.move_without_food > 100:
                self.fitness_score = -500
                break

            max_index = np.argmax(self.reaction)
            if max_index == 0:
                self.head_direction = 'up'
            elif max_index == 1:
                self.head_direction = 'right'
            elif max_index == 2:
                self.head_direction = 'down'
            elif max_index == 3:
                self.head_direction = 'left'

            self.move_snake_head()

            if self.possible_move() == False:
                self.snake_isAlive = False
                self.fitness_score -= 300
                break

            if self.there_is_food():
                self.snake_move_and_grow()
                self.new_food()
                self.move_without_food = 0
                self.fitness_score += 200
            else:
                self.snake_move()
                self.move_without_food += 1
                self.fitness_score += 10

            self.snake_sens_data = snake_sense.sense(self.level, self.body_positions, self.head_position, self.head_direction)
            self.reaction = net.forward(self.snake_sens_data)

        return self.fitness_score
