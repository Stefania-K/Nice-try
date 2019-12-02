import curses

from life import GameOfLife
from ui import UI
from time import sleep


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        for i in range(1, self.life.rows):
            for j in range(1, self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(j, i, '*')
                elif self.life.curr_generation[i][j] == 0:
                    screen.addstr(j, i, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        while (self.life.is_max_generations_exceed is False) and (self.life.is_changing is True):
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            sleep(1)
            self.life.step()
        screen.refresh()
        curses.endwin()


if __name__ == '__main__':
    gui = Console(GameOfLife((20, 10), True, 8))
    gui.run()