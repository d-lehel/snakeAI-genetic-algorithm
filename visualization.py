import pygame

pygame.init()
screen = pygame.display.set_mode((1500, 900))
clock = pygame.time.Clock()
snake_color = pygame.Color('green')
level_color = pygame.Color((30, 30, 30))
food_color = pygame.Color('red')
snake_body_rect = pygame.Rect(50, 50, 50, 50)

def draw(level, snake_sens_data, snake_sens_data_labels, fitness_score):
    
    # draw window background
    screen.fill( pygame.Color('black'))
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
    font_name =  pygame.font.get_default_font()
    font =  pygame.font.SysFont(font_name, font_size, bold=False)
    
    for i in range(len(snake_sens_data)):
            # set the text properties - binary data
            text_surface = font.render(snake_sens_data_labels[i] + str(snake_sens_data[i]), True, font_color)
            # get the text surface dimensions
            text_width, text_height = text_surface.get_size()
        
            # draw the text on the screen - data
            screen.blit(text_surface, (500, 40 + (i*26)))
        
    # # debug
    # text_surface = font.render(debug_text, True, font_color)
    # screen.blit(text_surface, (800, 650))
    
    # score
    text_surface = font.render('score: '+str(fitness_score), True, font_color)
    screen.blit(text_surface, (600, 650))