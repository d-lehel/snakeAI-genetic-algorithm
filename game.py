import pygame
import sys

class Snake:
    def __init__(self):
        self.body_X = [3,3,3]
        self.body_Y = [10,11,12]
        self.head = [self.body_X[-1:][0],self.body_Y[-1:][0]]
        self.direction = 'left'

    def modify_coordinates(self,x,y):
        # snake appear
        self.body_X.append(x)
        self.body_Y.append(y)
        # snake dissapear
        self.body_X.pop(0)
        self.body_Y.pop(0)
        # new head position
        self.head = [self.body_X[-1:][0],self.body_Y[-1:][0]]

pygame.init()
screen = pygame.display.set_mode((1500, 900))
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))

snake_color = pygame.Color('green')
level_color = pygame.Color((30,30,30))
food_color = pygame.Color('red')
snake_body_rect = pygame.Rect(50, 50, 50, 50)

move=0

snake = Snake()

while True:
    # in every loop check all event - like button presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = 'up'
            if event.key == pygame.K_DOWN:
                snake.direction = 'down'
            if event.key == pygame.K_LEFT:
                snake.direction = 'left'
            if event.key == pygame.K_RIGHT:
                snake.direction = 'right'

    screen.fill(pygame.Color('black'))
    # screen.fill((175,215,70)) rgb color

    # put surface on screen
    #screen.blit(test_surface, (300, 300))
    pygame.draw.rect(screen, level_color, pygame.Rect(600, 100, 500, 500))
    pygame.draw.rect(screen, snake_color, pygame.Rect(600+move, 100, 50, 50))
    pygame.draw.rect(screen, food_color, pygame.Rect(700, 300, 50, 50))
    
    # set the circle properties
    circle_color = (155, 155, 155)   # white color
    circle_radius = 25               # 50/2

    # set the first circle position
    circle1_pos = (100, 200)

    # set the second circle position
    circle2_pos = (300, 200)

    # draw the circles
    pygame.draw.circle(screen, circle_color, circle1_pos, circle_radius, 2)
    pygame.draw.circle(screen, circle_color, circle2_pos, circle_radius, 2)

    # draw the line connecting the circles
    line_color = (155, 155, 155)    # red color
    line_width = 2
    pygame.draw.line(screen, line_color, (125, 200), (275, 200), line_width)
    
    # font font font
    # set the font properties
    font_size = 24
    font_color = (255, 255, 255)   # white color
    font_name = pygame.font.get_default_font()
    font = pygame.font.SysFont(font_name, font_size, bold=False)

    # set the text properties
    text = "Hello, world!"
    text_surface = font.render(text, True, font_color)

    # get the text surface dimensions
    text_width, text_height = text_surface.get_size()

    # center the text on the screen
    text_x = 50
    text_y = 50

    # draw the text on the screen
    screen.blit(text_surface, (text_x, text_y))

    move+=50

    # draw all my elements in infinite loop
    pygame.display.update()

    # I set the game speed
    clock.tick(2)
