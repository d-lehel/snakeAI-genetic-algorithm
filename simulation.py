import random
import numpy as np
import snake_sense

def towards_food(head_position, head_direction, food_position):
    if head_direction == 'up' and food_position[0] < head_position[0]:
        return True
    if head_direction == 'down' and food_position[0] > head_position[0]:
        return True
    if head_direction == 'left' and food_position[1] < head_position[1]:
        return True
    if head_direction == 'right' and food_position[1] > head_position[1]:
        return True
    return False

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


def new_food(level, food_position, food_positions, apple_generate, same_construct):
    
    if same_construct:
        level[food_position[0]][food_position[1]] = 0
        food_position = food_positions[apple_generate]
        apple_generate += 1  
        
        while (level[food_position[0]][food_position[1]] != 0):
            apple_generate += 1  
            food_position = food_positions[apple_generate]
        level[food_position[0]][food_position[1]] = 2  
                  
    else:
        level[food_position[0]][food_position[1]] = 0
        food_position = [random.randint(0, 9), random.randint(0, 9)]
        while (level[food_position[0]][food_position[1]] != 0):
            food_position = [random.randint(0, 9), random.randint(0, 9)]
        level[food_position[0]][food_position[1]] = 2


def gameplay(net, visualization, same_construct, speed):

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
    apple_count = 1
    apple_generate = 0
    
    food_positions = [[3, 5], [2, 2], [3, 4], [7, 6], [8, 5], [2, 5], [9, 5], [8, 6], [7, 5], [6, 8],
                    [1, 2], [3, 3], [6, 0], [2, 1], [3, 8], [0, 3], [9, 9], [8, 8], [1, 4], [4, 1],
                    [4, 4], [9, 4], [4, 2], [2, 4], [4, 0], [5, 4], [6, 7], [9, 2], [1, 8], [2, 3],
                    [3, 7], [8, 9], [9, 6], [7, 1], [0, 6], [6, 5], [1, 6], [7, 3], [8, 7], [3, 5],
                    [5, 2], [6, 2], [5, 1], [5, 8], [5, 7], [0, 5], [8, 1], [1, 9], [6, 3], [5, 0],
                    [7, 2], [1, 5], [0, 7], [9, 1], [0, 8], [4, 5], [4, 8], [4, 6], [9, 0], [2, 8],
                    [8, 4], [3, 6], [6, 9], [7, 9], [5, 6], [0, 0], [3, 0], [5, 9], [9, 7], [2, 6],
                    [6, 6], [7, 0], [1, 7], [8, 0], [1, 1], [2, 7], [4, 7], [3, 2], [0, 1], [9, 3],
                    [1, 0], [6, 4], [4, 9], [3, 9], [7, 4], [5, 5], [2, 0], [8, 2], [0, 2], [9, 8],
                    [5, 3], [4, 3], [1, 3], [6, 1], [2, 9], [3, 1], [0, 4], [8, 3], [9, 8], [7, 8]]

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

    new_food(level, food_position, food_positions, apple_generate, same_construct)

    while isAlive:
        if move_without_food > 100:
            isAlive = False
            fitness_score = -1000
            # fitness score test
            if visualization == True:
                v.draw(level,head_position, snake_sens_data,
                       snake_sens_data_labels, fitness_score, reaction)
                v.pygame.display.update()
                v.clock.tick(1)
            break

        max_index = np.argmax(reaction)
        if max_index == 0:
            if head_direction != 'down' and head_direction != 'up':
                head_direction = 'up'
                # obstacle avoiding vertical
                # if head_position[1] == 0 or head_position[1] == 9:
                #     fitness_score += 200
                
        elif max_index == 1:
            if head_direction != 'left' and head_direction != 'right':
                head_direction = 'right'
                # obstacle avoiding horizontal
                # if head_position[0] == 0 or head_position[0] == 9:
                #     fitness_score += 200 
                
        elif max_index == 2:
            if head_direction != 'up' and head_direction != 'down':
                head_direction = 'down'
                # obstacle avoiding vertical
                # if head_position[1] == 0 or head_position[1] == 9:
                #     fitness_score += 200 
            
        elif max_index == 3:
            if head_direction != 'right' and head_direction != 'left':
                head_direction = 'left'
                # obstacle avoiding horizontal
                # if head_position[0] == 0 or head_position[0] == 9:
                #     fitness_score += 200 

        # the snake move towards food
        if towards_food(head_position, head_direction, food_position):
            fitness_score +=20
        else:
            fitness_score-=30
            
        move_snake_head(head_position, head_direction)

        if possible_move(level, head_position) == False:
            isAlive = False
            fitness_score -= 1000
            if visualization == True:
                v.draw(level, head_position, snake_sens_data,
                       snake_sens_data_labels, fitness_score, reaction)
                v.pygame.display.update()
                v.clock.tick(1)
            break

        if there_is_food(level, head_position):
            snake_move_and_grow(level, body_positions, head_position)
            new_food(level, food_position, food_positions, apple_generate, same_construct)
            
            move_without_food = 0
            fitness_score += 1500 * apple_count
            apple_count += 1
        else:
            snake_move(level, body_positions, head_position)
            move_without_food += 1

        snake_sens_data = snake_sense.sense(
            level, body_positions, head_position, head_direction)
        reaction = net.forward(snake_sens_data)

        if visualization == True:
            v.draw(level, head_position, snake_sens_data,
                   snake_sens_data_labels, fitness_score, reaction)
            v.pygame.display.update()
            v.clock.tick(speed)

    return fitness_score
