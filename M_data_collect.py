import random
import numpy as np
import snake_sense
import pickle


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


def gameplay():

    import visualization as v
    snake_sens_data = []
    snake_sens_data_labels = ['↖ ', '↖ ', '↖ ', '↑ ', '↑ ', '↑ ', '↗ ', '↗ ', '↗ ', '→ ', '→ ', '→ ', '↘ ', '↘ ',
                                '↘ ', '↓ ', '↓ ', '↓ ', '↙ ', '↙ ', '↙ ', '← ', '← ', '← ', '↑ ', '→ ', '↓ ', '← ', '↑ ', '→ ', '↓ ', '← ']

    input_data = []
    target_data = []

    isAlive = True
    head_position = [2, 2]
    body_positions = [[2, 2]]
    head_direction = 'right'
    food_position = [0, 0]
    fitness_score = 0
    speed = 4
    import pygame

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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    head_direction = 'up'
                if event.key == pygame.K_DOWN:
                    head_direction = 'down'
                if event.key == pygame.K_LEFT:
                    head_direction = 'left'
                if event.key == pygame.K_RIGHT:
                    head_direction = 'right'
        

        move_snake_head(head_position, head_direction)

        if possible_move(level, head_position) == False:
            isAlive = False
            v.draw(level, snake_sens_data,
                    snake_sens_data_labels, fitness_score, np.array([0, 0, 0, 0]))
            v.pygame.display.update()
            v.clock.tick(1)
            break

        if there_is_food(level, head_position):
            snake_move_and_grow(level, body_positions, head_position)
            new_food(level, food_position)
        else:
            snake_move(level, body_positions, head_position)

        snake_sens_data = snake_sense.sense(
            level, body_positions, head_position, head_direction)
        
        if head_direction == 'up':
            reaction = [1,0,0,0]
        if head_direction == 'right':
            reaction = [0,1,0,0]
        if head_direction == 'down':
            reaction = [0,0,1,0]
        if head_direction == 'left':
            reaction = [0,0,0,1]
            
        input_data.append(snake_sens_data)
        target_data.append(reaction)

        v.draw(level, snake_sens_data,
                snake_sens_data_labels, fitness_score, np.array([0, 0, 0, 0]))
        v.pygame.display.update()
        v.clock.tick(speed)

    # open last saved data
    last_input_data = []
    last_target_data = []
    with open('training_data.pickle', 'rb') as f:
        data = pickle.load(f)
        last_input_data = data[0]
        last_target_data = data[1]
        
    # after death, save out the data
    input_data = np.array(input_data)
    target_data = np.array(target_data)
    
    input_data = np.concatenate((input_data, last_input_data))
    target_data = np.concatenate((target_data, last_target_data))

    with open('training_data.pickle', 'wb') as f:
        pickle.dump([input_data, target_data], f)
        print('data saved! size: ', len(input_data))
    
gameplay()