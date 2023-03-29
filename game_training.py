import sys
import random
import numpy as np
import pickle

output = [0,0,0,0]
snake_isAlive = True
speed = 5.0
snake_head_pos = [2, 2]
snake_body_pos = [[2, 2]]
snake_head_direction = 'right'
snake_tail_direction = 'right'
food_pos = [7, 7]
snake_sens_data = []

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
    print('snake move and grow',snake_body_pos)
    # body move
    snake_body_pos.append(snake_head_pos.copy())
    # insert into the level
    level[snake_head_pos[0]][snake_head_pos[1]] = 1

def snake_move():
    print('snake move',snake_body_pos)
    # insert new head pos into the body
    snake_body_pos.append(snake_head_pos.copy())
    # insert into new head pos into the level
    level[snake_head_pos[0]][snake_head_pos[1]] = 1
    
    # remove tail from level
    level[snake_body_pos[0][0]][snake_body_pos[0][1]] = 0
    # remove tail from body
    snake_body_pos.pop(0)
    
level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def possible_move():
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


def there_is_food():
    if level[snake_head_pos[0]][snake_head_pos[1]] == 2:
        return True

def new_food():
    # solved, but why need global???
    global food_pos
    level[food_pos[0]][food_pos[1]]=1
    
    food_pos = [random.randint(0, 9), random.randint(0, 9)]
    while(level[food_pos[0]][food_pos[1]]!=0):
        food_pos = [random.randint(0, 9), random.randint(0, 9)]
        
    level[food_pos[0]][food_pos[1]]=2
    
#####################
#### snake sense ####
#####################

def snake_sense():
    data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   
    # up left
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        i -= 1
        j -= 1
        if (i < 0 or j < 0): # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[0] = 1
            
        if level[i][j] == 2: # I see food
            data[1] = 1
    
        if level[i][j] == 1: # I see my body
            data[2] = 1
          
    # up
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        i -= 1
        if i < 0: # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[3] = 1
            
        if level[i][j] == 2: # I see food
            data[4] = 1
    
        if level[i][j] == 1: # I see my body
            data[5] = 1
        
    # up right
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        i -= 1
        j += 1
        if (i < 0  or j > 7): # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[6] = 1
            
        if level[i][j] == 2: # I see food
            data[7] = 1
    
        if level[i][j] == 1: # I see my body
            data[8] = 1
        
    # right
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        j += 1
        if j > 7: # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[9] = 1
            
        if level[i][j] == 2: # I see food
            data[10] = 1
    
        if level[i][j] == 1: # I see my body
            data[11] = 1
        
    # down right
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        i += 1
        j += 1
        if (i > 7 or j > 7): # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[12] = 1
            
        if level[i][j] == 2: # I see food
            data[13] = 1
    
        if level[i][j] == 1: # I see my body
            data[14] = 1
        
    # down
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        i += 1
        if i > 7: # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[15] = 1
            
        if level[i][j] == 2: # I see food
            data[16] = 1
    
        if level[i][j] == 1: # I see my body
            data[17] = 1
        
    # down left
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        i += 1
        j -= 1
        if (i > 7 or j < 0): # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[18] = 1
            
        if level[i][j] == 2: # I see food
            data[19] = 1
    
        if level[i][j] == 1: # I see my body
            data[20] = 1
        
    # left
    i = snake_head_pos[0]
    j = snake_head_pos[1]
    while True:
        j -= 1
        if j < 0: # I see wall
            break
        if level[i][j] == 0: # I see distance
            data[21] = 1
            
        if level[i][j] == 2: # I see food
            data[22] = 1
    
        if level[i][j] == 1: # I see my body
            data[23] = 1
    
    global debug_text
    if len(snake_body_pos) == 1:
        snake_tail_direction = snake_head_direction
    else:
        if snake_body_pos[1][0] < snake_body_pos[0][0]: # i pos
            snake_tail_direction = 'up'
        if snake_body_pos[1][0] > snake_body_pos[0][0]: # i pos
            snake_tail_direction = 'down'
        if snake_body_pos[1][1] < snake_body_pos[0][1]: # j pos
            snake_tail_direction = 'left'
        if snake_body_pos[1][1] > snake_body_pos[0][1]: # j pos
            snake_tail_direction = 'right'
    
    data[24] = 1 if snake_head_direction == 'up' else 0
    data[25] = 1 if snake_head_direction == 'right' else 0
    data[26] = 1 if snake_head_direction == 'down' else 0
    data[27] = 1 if snake_head_direction == 'left' else 0
    
    data[28] = 1 if snake_tail_direction == 'up' else 0
    data[29] = 1 if snake_tail_direction == 'right' else 0
    data[30] = 1 if snake_tail_direction == 'down' else 0
    data[31] = 1 if snake_tail_direction == 'left' else 0
    
    return data # binary array

################
### GAMEPLAY ###
################

def gameplay(net):
    global snake_isAlive,snake_head_direction,snake_sens_data,output
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
            
        if there_is_food():
            snake_move_and_grow() 
            new_food()
        else:
            snake_move()
            
        # evaluate last move
        # todo    
            
        # snake sense
        snake_sens_data = snake_sense()  
        #snake think
        output = net.forward(snake_sens_data)
    
    return 1