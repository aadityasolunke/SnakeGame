import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    D = 1
    A = 2
    W = 3
    S = 4
    
Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        self.direction = Direction.D
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self.game_over = False
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.direction = Direction.A
                elif event.key == pygame.K_d:
                    self.direction = Direction.D
                elif event.key == pygame.K_w:
                    self.direction = Direction.W
                elif event.key == pygame.K_s:
                    self.direction = Direction.S
                elif event.key == pygame.K_RETURN and self.game_over:
                    self.__init__()  # Restart the game
        
        if not self.game_over:
            self._move(self.direction)
            self.snake.insert(0, self.head)
        
            self.game_over = self._is_collision()
            if self.game_over:
                return self.game_over, self.score
                
            if self.head == self.food:
                self.score += 1
                self._place_food()
            else:
                self.snake.pop()
        
        self._update_ui()
        self.clock.tick(SPEED)
        return self.game_over, self.score
    
    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        if self.game_over:
            text = font.render("Press ENTER to play again", True, WHITE)
            self.display.blit(text, [self.w // 2 - 170, self.h // 2])
        
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.D:
            x += BLOCK_SIZE
        elif direction == Direction.A:
            x -= BLOCK_SIZE
        elif direction == Direction.S:
            y += BLOCK_SIZE
        elif direction == Direction.W:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            print('Final Score:', score)
            pygame.time.wait(3000)  # Wait for 3 seconds before closing the window
            break
        
   # pygame.quit()
