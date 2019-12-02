import pygame
import pathlib
import random
from typing import Tuple, List, Optional

from copy import deepcopy
from pygame.locals import *


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]

class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cur_color = pygame.Color('white')
                if self.grid[i][j]:
                    cur_color = pygame.Color('green')
                pygame.draw.rect(self.screen, cur_color,
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        row, col = cell
        res = []
        if row > 0:
            res.append(self.grid[row - 1][col])
            if col > 0:
                res.append(self.grid[row - 1][col - 1])
            if col < self.cell_width - 1:
                res.append(self.grid[row - 1][col + 1])

        if row < self.cell_height - 1:
            res.append(self.grid[row + 1][col])
            if col > 0:
                res.append(self.grid[row + 1][col - 1])
            if col < self.cell_width - 1:
                res.append(self.grid[row + 1][col + 1])

        if col > 0:
            res.append(self.grid[row][col - 1])
        if col < self.cell_width - 1:
            res.append(self.grid[row][col + 1])

        # print(res)
        return res

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        alive = []
        dead = []

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if neighbours < 2 or neighbours > 3:
                    dead.append((i, j))
                elif neighbours == 3 and self.grid[i][j] == 0:
                    alive.append((i, j))

        for t in alive:
            self.grid[t[0]][t[1]] = 1
        for t in dead:
            self.grid[t[0]][t[1]] = 0
        return self.grid


if __name__ == '__main__':
    game = GameOfLife(240, 240, 20)
    game.run()