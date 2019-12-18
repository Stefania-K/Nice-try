import pygame


from pygame.locals import *
from ui import UI
from life import GameOfLife


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=5) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                color = pygame.Color('cyan')
                if self.life.curr_generation[i][j] == 1:
                    color = pygame.Color('purple4')
                pygame.draw.rect(self.screen, color, (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.life.create_grid(randomize = False)

        pause = True
        running = True
        while running and (self.life.is_max_generations_exceed is False):
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONUP:
                    i, j = event.pos
                    i = i // self.cell_size
                    j = j // self.cell_size
                    if self.life.curr_generation[j][i] == 0:
                        self.life.curr_generation[j][i] = 1
                    else:
                        self.life.curr_generation[j][i] = 0
                    self.draw_grid()
                    pygame.display.flip()

            if pause:
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                continue

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()





if __name__ == '__main__':
    ui = GUI(GameOfLife((50, 50), True, 1000))
    ui.run()