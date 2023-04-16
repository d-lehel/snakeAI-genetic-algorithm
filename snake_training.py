import random
import numpy as np
import snake_sense


def move_snake_head(head_position, head_direction):
    if head_direction == 'up':
        head_position[0] -= 1
    if head_direction == 'down':
        head_position[0] += 1
    if head_direction == 'left':
        head_position[1] -= 1
    if head_direction == 'right':
        head_position[1] += 1


def snake_move_and_grow(level, body_positions, head_position):
    body_positions.append(head_position.copy())
    level[head_position[0]][head_position[1]] = 1


def snake_move(level, body_positions, head_position):
    body_positions.append(head_position.copy())
    level[head_position[0]][head_position[1]] = 1
    level[body_positions[0][0]][body_positions[0][1]] = 0
    body_positions.pop(0)


def possible_move(level, head_position):
    if (head_position[0] < 0 or
        head_position[1] < 0 or
        head_position[0] > 9 or
            head_position[1] > 9):
        return False
    if level[head_position[0]][head_position[1]] == 1:
        return False


def there_is_food(level, head_position):
    if level[head_position[0]][head_position[1]] == 2:
        return True


def new_food(level, food_position):
    level[food_position[0]][food_position[1]] = 0
    food_position = [random.randint(0, 9), random.randint(0, 9)]
    while (level[food_position[0]][food_position[1]] != 0):
        food_position = [random.randint(0, 9), random.randint(0, 9)]
    level[food_position[0]][food_position[1]] = 2


def gameplay(net, visualization):

    if visualization == True:
        import visualization as v
        snake_sens_data = []
        snake_sens_data_labels = ['↖ ', '↖ ', '↖ ', '↑ ', '↑ ', '↑ ', '↗ ', '↗ ', '↗ ', '→ ', '→ ', '→ ', '↘ ', '↘ ',
                                  '↘ ', '↓ ', '↓ ', '↓ ', '↙ ', '↙ ', '↙ ', '← ', '← ', '← ', '↑ ', '→ ', '↓ ', '← ', '↑ ', '→ ', '↓ ', '← ']

    reaction = [0, 1, 0, 0]
    isAlive = True
    move_without_food = 0
    head_position = [2, 2]
    body_positions = [[2, 2]]
    head_direction = 'right'
    food_position = [0, 0]
    fitness_score = 0
    speed = 10

    level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    new_food(level, food_position)

    while isAlive:
        if move_without_food > 100:
            isAlive = False
            fitness_score = -1000
            # fitness score test
            if visualization == True:
                v.draw(level, snake_sens_data,
                       snake_sens_data_labels, fitness_score, reaction)
                v.pygame.display.update()
                v.clock.tick(1)
            break

        max_index = np.argmax(reaction)
        if max_index == 0:
            if head_direction != 'down' and head_direction != 'up':
                head_direction = 'up'
                # obstacle avoiding vertical
                if head_position[1] == 0 or head_position[1] == 9:
                    fitness_score += 200
                
        elif max_index == 1:
            if head_direction != 'left' and head_direction != 'right':
                head_direction = 'right'
                # obstacle avoiding horizontal
                if head_position[0] == 0 or head_position[0] == 9:
                    fitness_score += 200 
                
        elif max_index == 2:
            if head_direction != 'up' and head_direction != 'down':
                head_direction = 'down'
                # obstacle avoiding vertical
                if head_position[1] == 0 or head_position[1] == 9:
                    fitness_score += 200 
            
        elif max_index == 3:
            if head_direction != 'right' and head_direction != 'left':
                head_direction = 'left'
                # obstacle avoiding horizontal
                if head_position[0] == 0 or head_position[0] == 9:
                    fitness_score += 200 

        move_snake_head(head_position, head_direction)

        if possible_move(level, head_position) == False:
            isAlive = False
            # fitness_score -= 1000
            if visualization == True:
                v.draw(level, snake_sens_data,
                       snake_sens_data_labels, fitness_score, reaction)
                v.pygame.display.update()
                v.clock.tick(1)
            break

        if there_is_food(level, head_position):
            snake_move_and_grow(level, body_positions, head_position)
            new_food(level, food_position)
            move_without_food = 0
            fitness_score += 1000
        else:
            snake_move(level, body_positions, head_position)
            move_without_food += 1
            fitness_score += 10

        snake_sens_data = snake_sense.sense(
            level, body_positions, head_position, head_direction)
        reaction = net.forward(snake_sens_data)

        if visualization == True:
            v.draw(level, snake_sens_data,
                   snake_sens_data_labels, fitness_score, reaction)
            v.pygame.display.update()
            v.clock.tick(speed)

    return fitness_score
