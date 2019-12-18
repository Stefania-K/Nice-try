import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        for i in range(self.life.cols+2):
            if i == 0 or i == self.life.cols+1:
                screen.addstr(0, i, '+')
            else:
                screen.addstr(0, i, '-')
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.life.cols + 1, '|')
        for i in range(self.life.cols + 2):
            if i == 0 or i == self.life.cols + 1:
                screen.addstr(self.life.rows + 1, i, '+')
            else:
                screen.addstr(self.life.rows + 1, i, '-')

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, '*')
                else: 
                    screen.addstr(i + 1, j + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()
        time.sleep(1)
        while not self.life.is_max_generations_exceed and self.life.is_changing:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(1)
        screen.clear()
        curses.endwin()