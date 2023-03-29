import random
import numpy as np
import snake_sense

output = [0, 0, 0, 0]
snake_isAlive = True
speed = 5.0
snake_head_pos = [2, 2]
snake_body_pos = [[2, 2]]
snake_head_direction = 'right'
snake_tail_direction = 'right'
food_pos = [7, 7]
snake_sens_data = []
fitness_score = 0


def move_snake_head():
    if snake_head_direction == 'up':
        snake_head_pos[0] -= 1
    if snake_head_direction == 'down':
        snake_head_pos[0] += 1
    if snake_head_direction == 'left':
        snake_head_pos[1] -= 1
    if snake_head_direction == 'right':
        snake_head_pos[1] += 1


def snake_move_and_grow():
    print('snake move and grow', snake_body_pos)
    # body move
    snake_body_pos.append(snake_head_pos.copy())
    # insert into the level
    level[snake_head_pos[0]][snake_head_pos[1]] = 1


def snake_move():
    # insert new head pos into the body
    snake_body_pos.append(snake_head_pos.copy())
    # insert into new head pos into the level
    level[snake_head_pos[0]][snake_head_pos[1]] = 1

    # remove tail from level
    level[snake_body_pos[0][0]][snake_body_pos[0][1]] = 0
    # remove tail from body
    snake_body_pos.pop(0)


level = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 2, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]


def possible_move():
    global fitness_score
    # colision - walls
    if (snake_head_pos[0] < 0 or
        snake_head_pos[1] < 0 or
        snake_head_pos[0] > 9 or
            snake_head_pos[1] > 9):
        print("game over -> wall")
        return False

    # colision - body
    if level[snake_head_pos[0]][snake_head_pos[1]] == 1:
        print("game over -> body")
        return False
    
    # + fitness score for new positions
    if level[snake_head_pos[0]][snake_head_pos[1]] == 3:
        fitness_score += 10


def there_is_food():
    if level[snake_head_pos[0]][snake_head_pos[1]] == 2:
        return True


def new_food():
    # solved, but why need global???
    global food_pos
    level[food_pos[0]][food_pos[1]] = 1

    food_pos = [random.randint(0, 9), random.randint(0, 9)]
    while (level[food_pos[0]][food_pos[1]] != 0):
        food_pos = [random.randint(0, 9), random.randint(0, 9)]

    level[food_pos[0]][food_pos[1]] = 2


def calculate_fitness():
    pass

################
### GAMEPLAY ###
################


def gameplay(net):
    global snake_isAlive, snake_head_direction, snake_sens_data, output, fitness_score
    while snake_isAlive:
        # determine the brain output
        max_index = np.argmax(output)
        if max_index == 0:
            snake_head_direction = 'up'
        elif max_index == 1:
            snake_head_direction = 'right'
        elif max_index == 2:
            snake_head_direction = 'down'
        elif max_index == 3:
            snake_head_direction = 'left'

        move_snake_head()

        if possible_move() == False:
            snake_isAlive = False
            fitness_score -= 200
            break

        if there_is_food():
            snake_move_and_grow()
            new_food()
            fitness_score += 100
        else:
            snake_move()
            fitness_score += 5

        # evaluate last move
        calculate_fitness()

        # snake sense
        snake_sens_data = snake_sense.sense(
            level, snake_body_pos, snake_head_pos, snake_head_direction)
        # snake think
        output = net.forward(snake_sens_data)

    return fitness_score
