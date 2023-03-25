import pygame
import sys
import random
import numpy as np

####################
#### neural net ####
####################

class NeuralNet:
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size):
        # Initialize the weights and biases for the first hidden layer
        self.weights1 = np.random.randn(input_size, hidden_size1)
        self.biases1 = np.random.randn(hidden_size1)* 0.1 # ???
        
        # Initialize the weights and biases for the second hidden layer
        self.weights2 = np.random.randn(hidden_size1, hidden_size2)
        self.biases2 = np.random.randn(hidden_size2)* 0.1
        
        # Initialize the weights and biases for the output layer
        self.weights3 = np.random.randn(hidden_size2, output_size)
        self.biases3 = np.random.randn(output_size)* 0.1
    
    def forward(self, x):
        # Forward pass through the network
        hidden_layer1 = np.maximum(0, np.dot(x, self.weights1) + self.biases1)
        hidden_layer2 = np.maximum(0, np.dot(hidden_layer1, self.weights2) + self.biases2)
        output_layer = np.dot(hidden_layer2, self.weights3) + self.biases3
        return output_layer
    
####################
#### snake mind ####
####################
    
# input size = 32, hidden size1 = 24, hidden size2 = 12, output size = 4
net = NeuralNet(32, 24, 12, 4) 
output = [0,0,0,0]

snake_isAlive = True
speed = 5.0
snake_head_pos = [2, 2]
snake_body_pos = [[2, 2]]
snake_head_direction = 'right'
snake_tail_direction = 'right'
food_pos = [7, 7]
snake_sens_data = []
snake_sens_data_labels = ['↖ ','↖ ','↖ ','↑ ','↑ ','↑ ','↗ ','↗ ','↗ ','→ ','→ ','→ ','↘ ','↘ ','↘ ','↓ ','↓ ','↓ ','↙ ','↙ ','↙ ','← ','← ','← ','↑ ','→ ','↓ ','← ','↑ ','→ ','↓ ','← ']

debug_text = 'debug text'

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


def set_draw():
    # draw window background
    screen.fill(pygame.Color('black'))
    # draw level background
    pygame.draw.rect(screen, level_color, pygame.Rect(600, 100, 500, 500))

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.rect(screen, snake_color,
                                 pygame.Rect(((j+1)*50)+550, ((i+1)*50)+50, 50, 50))
            if level[i][j] == 2:
                pygame.draw.rect(screen, food_color,
                                 pygame.Rect(((j+1)*50)+550, ((i+1)*50)+50, 50, 50))
    # font           
    font_size = 30
    font_color = (255, 255, 255)   # white color
    font_name = pygame.font.get_default_font()
    font = pygame.font.SysFont(font_name, font_size, bold=False)
    
    for i in range(len(snake_sens_data)):
        # set the text properties - binary data
        text = snake_sens_data_labels[i] + str(snake_sens_data[i])
        text_surface = font.render(text, True, font_color)
        # get the text surface dimensions
        text_width, text_height = text_surface.get_size()
        # center the text on the screen
        text_x = 500
        text_y = 40 + (i*26)
        # draw the text on the screen - data
        screen.blit(text_surface, (text_x, text_y))
    
        
        # debug
        text = debug_text
        text_surface = font.render(text, True, font_color)
        text_x = 700
        text_y = 700 
        screen.blit(text_surface, (text_x, text_y))

def new_food():
    # solved, but why need global???
    global food_pos
    level[food_pos[0]][food_pos[1]]=1
    
    food_pos = [random.randint(0, 9), random.randint(0, 9)]
    while(level[food_pos[0]][food_pos[1]]!=0):
        food_pos = [random.randint(0, 9), random.randint(0, 9)]
        
    level[food_pos[0]][food_pos[1]]=2
    

pygame.init()
screen = pygame.display.set_mode((1500, 900))
clock = pygame.time.Clock()
snake_color = pygame.Color('green')
level_color = pygame.Color((30, 30, 30))
food_color = pygame.Color('red')
snake_body_rect = pygame.Rect(50, 50, 50, 50)

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

##################
### GAME LOGIC ###
##################


while True:
    while snake_isAlive:
        
        # set the game speed
        clock.tick(speed) 
        
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
        
        # in every loop check all event - like button presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_head_direction != 'down':
                    snake_head_direction = 'up'
                    break # to avoid too fast press
                if event.key == pygame.K_DOWN and snake_head_direction != 'up':
                    snake_head_direction = 'down'
                    break
                if event.key == pygame.K_LEFT and snake_head_direction != 'right':
                    snake_head_direction = 'left'
                    break
                if event.key == pygame.K_RIGHT and snake_head_direction != 'left':
                    snake_head_direction = 'right'
                    break
                if event.key == pygame.K_p: 
                    speed = 0.3 if speed == 5 else 5
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
           
        move_snake_head()
        
        if possible_move() == False:
            snake_isAlive = False
            pygame.quit()

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
        
            
        set_draw()

        # redraw all element
        pygame.display.update()


# sample for designing neural visualization

# # set the circle properties
# circle_color = (155, 155, 155)   # white color
# circle_radius = 25               # 50/2

# # set the first circle position
# circle1_pos = (100, 200)

# # set the second circle position
# circle2_pos = (300, 200)

# # draw the circles
# pygame.draw.circle(screen, circle_color, circle1_pos, circle_radius, 2)
# pygame.draw.circle(screen, circle_color, circle2_pos, circle_radius, 2)

# # draw the line connecting the circles
# line_color = (155, 155, 155)    # red color
# line_width = 2
# pygame.draw.line(screen, line_color, (125, 200), (275, 200), line_width)
