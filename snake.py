import pygame, sys, random
from pygame.math import Vector2

class Fruit():
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, (126, 166, 114), fuit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Snake():
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/body_part.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_part.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_part.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_part.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sounds/crunch_sound.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 or next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 or next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 or next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 or next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if   head_relation ==   Vector2(1,0):   self.head = self.head_left      # head to the left of body
        elif head_relation ==   Vector2(-1,0):  self.head = self.head_right      # head to the right of body
        elif head_relation ==   Vector2(0,1):   self.head = self.head_up     # head to the left of body
        elif head_relation ==   Vector2(0,-1):  self.head = self.head_down      # head to the left of body

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if   tail_relation ==   Vector2(1,0):   self.tail = self.tail_left      
        elif tail_relation ==   Vector2(-1,0):  self.tail = self.tail_right      
        elif tail_relation ==   Vector2(0,1):   self.tail = self.tail_up     
        elif tail_relation ==   Vector2(0,-1):  self.tail = self.tail_down              

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def reset(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(0, 0)
        
class Main():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision() 
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def check_fail(self):
        if (not 0 <= self.snake.body[0].x < CELL_NUMBER) or (not 0 <= self.snake.body[0].y < CELL_NUMBER):
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0: 
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 3, apple_rect.top - 3, apple_rect.width + score_rect.width + 6, apple_rect.height + 6)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

pygame.init()
clock = pygame.time.Clock()

# Display Setup
CELL_SIZE = 20
CELL_NUMBER = 30
bg_color = (175, 215, 70)
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
pygame.display.set_caption('Snake')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Fonts/PoetsenOne-Regular.ttf', 20)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)

    # Visuals
    screen.fill(bg_color)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
