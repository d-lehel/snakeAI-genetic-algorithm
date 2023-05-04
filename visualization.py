import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1500, 900))
clock = pygame.time.Clock()
snake_color = pygame.Color('green')
level_color = pygame.Color((240, 240, 240))
food_color = pygame.Color('red')
snake_body_rect = pygame.Rect(50, 50, 50, 50)

def draw(level, head_position, snake_sens_data, snake_sens_data_labels, fitness_score, reaction):
    
    # draw window background
    screen.fill( pygame.Color('white'))
    # draw level background
    pygame.draw.rect(screen, level_color, pygame.Rect(600, 100, 500, 500))

    for i in range(len(level)):
        for j in range(len(level[i])):
            if i == head_position[0] and j == head_position[1]:
                lines = False
                color = (150,150,150)
                # Set the starting point of the line
                start_point = (((j+1)*50)+575, ((i+1)*50)+75)
                # Draw the line
                pygame.draw.line(screen, color, start_point, (start_point[0]-500, start_point[1] - 500))
                pygame.draw.line(screen, color, start_point, (start_point[0], start_point[1] - 500))
                pygame.draw.line(screen, color, start_point, (start_point[0]+500, start_point[1] - 500))
                pygame.draw.line(screen, color, start_point, (start_point[0]+500, start_point[1] - 0))
                pygame.draw.line(screen, color, start_point, (start_point[0]+500, start_point[1] + 500))
                pygame.draw.line(screen, color, start_point, (start_point[0], start_point[1] + 500))
                pygame.draw.line(screen, color, start_point, (start_point[0]-500, start_point[1] + 500))
                pygame.draw.line(screen, color, start_point, (start_point[0]-500, start_point[1] - 0))
                                
                                
            if level[i][j] == 1:
                pygame.draw.rect(screen, snake_color,
                                    pygame.Rect(((j+1)*50)+550, ((i+1)*50)+50, 50, 50))
            if level[i][j] == 2:
                    pygame.draw.rect(screen, food_color,
                                    pygame.Rect(((j+1)*50)+550, ((i+1)*50)+50, 50, 50))
    # font           
    font_size = 30
    font_color = (0, 0, 0)   # white color
    font_name =  pygame.font.get_default_font()
    font =  pygame.font.SysFont(font_name, font_size, bold=False)
    
    for i in range(len(snake_sens_data)):
        # set the text properties - binary data
        text_surface = font.render(snake_sens_data_labels[i] + str(snake_sens_data[i]), True, font_color)
        # get the text surface dimensions
        text_width, text_height = text_surface.get_size()
    
        # draw the text on the screen - data
        screen.blit(text_surface, (40, 40 + (i*25)))
            
    # draw labels
    labels = ['up','right','down','left']
    for i in range(4):
        text_surface = font.render(str(labels[i]), True, font_color)
        text_width, text_height = text_surface.get_size()
        screen.blit(text_surface, (520, 340 + (i*50)))
        
    # # debug
    # text_surface = font.render(debug_text, True, font_color)
    # screen.blit(text_surface, (800, 650))
    
    # score
    text_surface = font.render('score: '+str(fitness_score), True, font_color)
    screen.blit(text_surface, (600, 650))
    
    # drawing neural network
    # Set the colors for the layers
    input_layer_color = (255, 255, 255)
    hidden_layer_color = (200, 200, 200)
    output_layer_color = (0, 0, 0)

    # Set the positions for the nodes in each layer
    input_layer_pos = [(100, y) for y in range(50, 850, 800 // 31)]
    hidden_layer_1_pos = [(270, y) for y in range(150, 700, 600 // 23)]
    hidden_layer_2_pos = [(400, y) for y in range(200, 650, 400 // 11)]
    output_layer_pos = [(500, y) for y in range(350, 550, 50)]

    

    # Draw the connections between the nodes
    for i, input_node in enumerate(input_layer_pos):
        for hidden_node in hidden_layer_1_pos:
            line_color = (200, 0, 0) if random.random() < 0.5 else (0, 0, 0)
            pygame.draw.line(screen, line_color, input_node, hidden_node)

    for i, hidden_node in enumerate(hidden_layer_1_pos):
        for output_node in hidden_layer_2_pos:
            line_color = (200, 0, 0) if random.random() < 0.5 else (0, 0, 0)
            pygame.draw.line(screen, line_color, hidden_node, output_node)

    for i, hidden_node in enumerate(hidden_layer_2_pos):
        for output_node in output_layer_pos:
            line_color = (200, 0, 0) if random.random() < 0.5 else (0, 0, 0)
            pygame.draw.line(screen, line_color, hidden_node, output_node)
            
    # Draw the nodes for the input layer
    for i in range(len(input_layer_pos)):
        if snake_sens_data[i] == 1:
            pygame.draw.circle(screen, (200, 0, 0), input_layer_pos[i], 10)
        else:
            pygame.draw.circle(screen, (00, 0, 0), input_layer_pos[i], 10)

    # Draw the nodes for the first hidden layer
    for pos in hidden_layer_1_pos:
        line_color = (200, 0, 0) if random.random() < 0.5 else (0, 0, 0)
        pygame.draw.circle(screen, line_color, pos, 10)

    # Draw the nodes for the second hidden layer
    for pos in hidden_layer_2_pos:
        line_color = (200, 0, 0) if random.random() < 0.5 else (0, 0, 0)
        pygame.draw.circle(screen, line_color, pos, 10)

    # Draw the nodes for the output layer
    index = reaction.argmax()
    for i in range(len(output_layer_pos)):
        if i == index:
            pygame.draw.circle(screen, (200,0,0), output_layer_pos[i], 10)
        else:
            pygame.draw.circle(screen, output_layer_color, output_layer_pos[i], 10)