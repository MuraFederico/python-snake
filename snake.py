from tarfile import BLOCKSIZE
import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('Arial', 24)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x y')

BLOCKSIZE = 20
SPEED = 10

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                        Point(self.head.x-BLOCKSIZE, self.head.y),
                        Point(self.head.x-2*BLOCKSIZE, self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        y = random.randint(0, (self.h-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()



    def play_step(self):
        #  collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

            

        # move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


        # return game over and score
        return game_over, self.score
    def _is_collision(self):
        # hits boundary 
        if self.head.x < 0 or self.head.x > self.w-BLOCKSIZE or self.head.y < 0 or self.head.y > self.h-BLOCKSIZE:
            return True
        # hits self
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill((0, 0, 0))
        for point in self.snake:
            pygame.draw.rect(self.display, (0, 0, 255), (point.x, point.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(self.display, (0, 100, 255), (point.x+4, point.y+4, 12, 12))

        pygame.draw.rect(self.display, (255, 0, 0), (self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        text = font.render('score: ', str(self.score), True, (255, 255, 255))
        self.display.blit(text, (0, 0))
        pygame.display.flip()

    def _move(self, direction):
        if direction == Direction.RIGHT:
            self.head = Point(self.head.x+BLOCKSIZE, self.head.y)
        elif direction == Direction.LEFT:
            self.head = Point(self.head.x-BLOCKSIZE, self.head.y)
        elif direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y-BLOCKSIZE)
        elif direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y+BLOCKSIZE)

if __name__ == '__main__':
    game = SnakeGame()

    #game loop

    while True:
        game_over, score = game.play_step()

        # break if game over
        if game_over == True:
            break

    print('final score:', score)

    pygame.quit()
