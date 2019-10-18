from typing import Tuple, List, Set, Optional


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    l = len(values) // n
    out = []
    last = 0
    while last < len(values):
        out.append(values[last:last + l])
        last += l
    return out


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            i, j = pos
    return grid[i]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    c = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            i, j = pos
    while i <= len(grid):
        c.append(grid[i][j])
        i += 1
    return c


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    c = []
    for ele in grid:
        ele = group(ele, 3)
    for i in range(len(grid)):
        if i in range(3):
            if j in range(3):
                for i in range(3):
                    for j in range(3):
                        c.append(grid[i][j])
        elif j in range(3, 6):
            for i in range(3):
                for j in range(3, 6):
                    C.append(grid[i][j])
        elif j in range(6, 9):
            for i in range(3):
                for j in range(6, 9):
                    c.append(grid[i][j])
    elif i in range(3, 6):
        if j in range(3):
            for i in range(3, 6):
                for j in range(3):
                    c.append(grid[i][j])
        elif j in range(3, 6):
            for i in range(3, 6):
                for j in range(3, 6):
                    c.append(grid[i][j])
        elif j in range(6, 9):
            for i in range(3, 6):
                for j in range(6, 9):
                    c.append(grid[i][j])
    elif i in range(6, 9):
        if j in range(3):
            for i in range(6, 9):
                for j in range(3):
                    c.append(grid[i][j])
        elif j in range(3, 6):
            for i in range(6, 9):
                for j in range(3, 6):
                    c.apppend(grid[i][j])
        elif j in range(6, 9):
            for i in range(6, 9):
                for j in range(6, 9):
                    c.append(grid[i][j])
    return c


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return (i, j)
    return None


def find_possible_values(grid, pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    pos_val = '123456789'
    values = []
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for l in pos_val:
        if l not in row and l not in col and l not in block:
            values.append(l)
    return set(str(values))


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    i, j = pos
    if not pos:
        return grid
    for value in find_possible_values(grid, pos):
        grid[i][j] = value
        solution = solve(grid)
        if solution:
            return solusion
    grid[i][j] = "."
    return None


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for i in range(len(solution)):
        i, 0 = pos
        row = set(get_row(solution, pos))
        if row != set('123456789'):
            return False

    for j in range(len(solution)):
        col = set(get_col(solution, (0, j)))
        if col != set('123456789'):
            return False

    for i in (0, 3, 6):
        for j in (0, 3, 6):
            block = set(get_block(solution, (i, j)))
            if block != set('123456789'):
                return False
    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([['.'] * 9 for _ in range(9)])
    N = 81 - min(81, max(0, N))
    while N:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if grid[i][j] != '.':
            grid[i][j] = '.'
            N -= 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
