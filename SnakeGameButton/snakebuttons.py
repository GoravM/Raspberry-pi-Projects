import pygame
import random
import sys
from signal import pause
from gpiozero import Button
from time import sleep

#initialize buttons and their respective gpio pins
upbutton =  Button(23)
rightbutton = Button(18)
leftbutton = Button(27)
downbutton = Button(17)
endbutton = Button(24)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

BLOCK_SIZE = 50


# Change the file directory to your own in order for it to work
FONT = pygame.font.Font("/home/gorav/Workspace/RaspProjs/SnakeGameButton/font.ttf", BLOCK_SIZE * 2)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
run = True

def drawGrid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen,(51, 51, 51), rect, 1)

class Snake:

    def __init__(self):
        self.x = BLOCK_SIZE
        self.y = BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.body = [pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.head = pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.dead = False
    
    def update(self):
        global apple
        # death
        for square in self.body:
            if (self.head.x == square.x and self.head.y == square.y):
                self.dead = True
            if (self.head.x not in range(0, SCREEN_WIDTH) or self.head.y not in range(0, SCREEN_HEIGHT)):
                self.dead = True

        if (self.dead):
            self.x = BLOCK_SIZE
            self.y = BLOCK_SIZE
            self.xdir = 1
            self.ydir = 0
            self.body = [pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.head = pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.dead = False
            apple = Apple()

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x = self.body[i+1].x
            self.body[i].y = self.body[i+1].y

        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

player = Snake()

class Apple:
    global player
    def __init__(self):
        self.x = int(random.randint(0, SCREEN_WIDTH)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SCREEN_HEIGHT)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):
        pygame.draw.rect(screen, "red", self.rect)


score = FONT.render("1", True, "white")
score_rect = score.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/20))

apple = Apple()

try:
    while(run):
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        
            # movement
            # in false put the joystick values 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.ydir != 1: 
                    player.ydir = -1
                    player.xdir = 0

                elif event.key == pygame.K_a and player.xdir != 1:
                    player.ydir = 0
                    player.xdir = -1

                elif event.key == pygame.K_s and player.ydir != -1:
                    player.ydir = 1
                    player.xdir = 0

                elif event.key == pygame.K_d and player.xdir != -1:
                    player.ydir = 0
                    player.xdir = 1
                elif event.key == pygame.K_ESCAPE:
                    run = False
                    
        # if there is no keyboard input event then it accepts button as input
        if upbutton.value == 1 and player.ydir != 1: 
            player.ydir = -1
            player.xdir = 0

        elif leftbutton.value == 1 and player.xdir != 1:
            player.ydir = 0
            player.xdir = -1

        elif downbutton.value == 1 and player.ydir != -1:
            player.ydir = 1
            player.xdir = 0

        elif rightbutton.value == 1 and player.xdir != -1:
            player.ydir = 0
            player.xdir = 1
        elif endbutton.value == 1:
            run = False
        
        clock.tick(1000)
        
        screen.fill((0,0,0))
        drawGrid()
        player.update()
        apple.update()
        
        score = FONT.render(f"{len(player.body) - 1}", True, "white")
        pygame.draw.rect(screen, "green", player.head)   
        screen.blit(score, score_rect) 
        
        for square in player.body:
            pygame.draw.rect(screen, "green", square)
        
        if (player.head.x == apple.x and player.head.y == apple.y):
            player.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple() # new apple
        
        pygame.display.update()

except KeyboardInterrupt:
    pass

finally:
    upbutton.close()
    rightbutton.close()
    leftbutton.close()
    downbutton.close()
    endbutton.close()
    pygame.quit()
    sys.exit()
