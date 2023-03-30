import pygame
import sys
import random
import numpy as np
import pickle
import snake_brain
import snake_sense

# input size = 32, hidden size1 = 24, hidden size2 = 12, output size = 4
net = snake_brain.NeuralNet(32, 24, 12, 4) 
output = [0,1,0,0]
snake_isAlive = True
speed = 5.0
score = 0
snake_head_pos = [2, 2]
snake_body_pos = [[2, 2]]
snake_head_direction = 'right'
snake_tail_direction = 'right'
food_pos = [5, 5]
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
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    
# pygame variables

pygame.init()
screen = pygame.display.set_mode((1500, 900))
clock = pygame.time.Clock()
snake_color = pygame.Color('green')
level_color = pygame.Color((30, 30, 30))
food_color = pygame.Color('red')
snake_body_rect = pygame.Rect(50, 50, 50, 50)

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
        text_surface = font.render(snake_sens_data_labels[i] + str(snake_sens_data[i]), True, font_color)
        # get the text surface dimensions
        text_width, text_height = text_surface.get_size()
    
        # draw the text on the screen - data
        screen.blit(text_surface, (500, 40 + (i*26)))
    
    # debug
    text_surface = font.render(debug_text, True, font_color)
    screen.blit(text_surface, (800, 650))
    
    # score
    text_surface = font.render('score: '+str(score), True, font_color)
    screen.blit(text_surface, (600, 650))


##################
### GAME LOGIC ###
##################

# load the best net from the file
with open('brains.pickle', 'rb') as f:
    nets = pickle.load(f)
net = nets[999]

while snake_isAlive:
    
    # set the game speed
    clock.tick(speed) 
    
    #determine the brain output
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
        break

    if there_is_food():
        snake_move_and_grow() 
        new_food()
        score +=1
    else:
        snake_move()
        
    # evaluate last move
    # todo    
        
    # snake sense
    snake_sens_data = snake_sense.sense(level, snake_body_pos, snake_head_pos, snake_head_direction)  
    #snake think
    output = net.forward(snake_sens_data) 
    
    set_draw()

    # redraw all element
    pygame.display.update()