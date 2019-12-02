import pygame
from pygame.locals import *
from ui import UI
from life import GameOfLife


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = life.cols * self.cell_size, life.rows * self.cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        width, height = self.screen_size

        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('white'),
                             (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('white'),
                             (0, y), (width, y))
    
    
    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                cur_color = pygame.Color('cyan')
                curr_generation = self.life.curr_generation
                if curr_generation[i][j] == 1:
                    cur_color = pygame.Color('purple4')
                pygame.draw.rect(self.screen, cur_color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))


    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        pause = False
        while running and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONDOWN and pause:
                    self.mouse_fill_cell()

            self.draw_grid()
            self.draw_lines()
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()



    def mouse_fill_cell(self) -> None:
        x, y = pygame.mouse.get_pos()
        col = x // self.cell_size
        row = y // self.cell_size
        self.life.curr_generation[row][col] = (self.life.curr_generation[row][col] + 1) % 2

if __name__ == '__main__':
    life = GameOfLife((50, 50), max_generations = 1000)
    gui = GUI(life)
    gui.run()