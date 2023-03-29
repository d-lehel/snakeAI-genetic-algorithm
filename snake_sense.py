def sense(level, snake_body_pos, snake_head_pos, snake_head_direction):
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