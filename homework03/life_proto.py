import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
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

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

    def create_grid(self, randomize: bool=False) -> Grid:
        grid = []
        for i in range(self.cols):
            grid.append([None] * self.rows)
        for i in range(self.cols):
            for j in range(self.rows):
                if randomize != 0:
                    grid[i][j] = random.randint(0, 1)
                else: 
                    grid[i][j] = 0
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        Cells = []
        if row > 0:
            Cells.append(self.curr_generation[row - 1][col])
            if col > 0:
                Cells.append(self.curr_generation[row - 1][col - 1])
            if col < (self.cols - 1):
                Cells.append(self.curr_generation[row - 1][col + 1])
        if row < (self.rows - 1):
            Cells.append(self.curr_generation[row + 1][col])
            if col > 0: 
                Cells.append(self.curr_generation[row + 1][col - 1])
            if col < (self.cols - 1):
                Cells.append(self.curr_generation[row + 1][col + 1])
        if col > 0:
            Cells.append(self.curr_generation[row][col - 1])
        if col < (self.cols - 1):
            Cells.append(self.curr_generation[row][col + 1])
        return Cells
        

    def get_next_generation(self) -> Grid:
        grid = deepcopy(self.curr_generation)
        dead = []
        alive = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (sum(self.get_neighbours((i, j))) == 3) and (self.curr_generation[i][j] == 0):
                    alive.append((i, j))
                elif (sum(self.get_neighbours((i, j))) < 2) or (sum(self.get_neighbours((i, j))) > 3):
                    dead.append((i, j))
        for i in alive:
            grid[i[0]][i[1]] = 1
        for i in dead:
            grid[i[0]][i[1]] = 0
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1


    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.n_generation >= self.max_generations:
            return True
        else:
            return False


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            False
        

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as f:
            lines = f.readlines()
            rows = len(lines)
            cols = len(lines[0].strip())
            game = GameOfLife(size = (rows, cols), randomize = False)

        with open(filename, 'r') as f:
            for i in range(rows):
                lines[i].split()
                for j in range(cols):
                    game.curr_generation[i][j] = int(lines[i][j])
        return game

        

    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            for row in self.rows:
                for ch in row:
                    f.write(''.join(str(ch)) + '\n')