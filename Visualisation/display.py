import curses
import random
from typing import List, Tuple, Dict, Any
from mazegen.generator import MazeGenerator
from mazegen.show_the_exit import find_the_way

COLOR_NAMES: List[str] = ["White", "Green", "Red", "Blue"]
PATTERN_COLOR_NAMES = ["Yellow", "Cyan", "Green BG", "Red BG"]

CELL_WIDTH = 5
CELL_HEIGHT = 2


def setup_colors() -> None:
    """Initialize color pairs for curses."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_MAGENTA)


def safe_addstr(stdscr: 'curses.window', y: int, x: int,
                text: str, attr: int) -> None:
    """Write text at position (y, x). Do nothing if out of bounds."""
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x < 0 or x + len(text) > max_x:
        return
    stdscr.addstr(y, x, text, attr)


def has_wall(cell_value: int, direction: str) -> bool:
    """Return True if the wall exists in the given direction."""
    if direction == 'N':
        return bool(cell_value & 1)
    if direction == 'E':
        return bool(cell_value & 2)
    if direction == 'S':
        return bool(cell_value & 4)
    if direction == 'W':
        return bool(cell_value & 8)
    return False


def draw_maze(stdscr: 'curses.window', maze: MazeGenerator,
              wall_color: int, pattern_color: int) -> None:
    """Draw the maze walls and cell contents on screen."""
    wall_attr = curses.color_pair(wall_color)
    entry_attr = curses.color_pair(6) | curses.A_BOLD
    pattern_attr = curses.color_pair(pattern_color)
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]

            screen_x = x * CELL_WIDTH
            screen_y = y * CELL_HEIGHT

            safe_addstr(stdscr, screen_y, screen_x, "██", wall_attr)

            if has_wall(cell, 'N'):
                safe_addstr(stdscr, screen_y, screen_x + 2, "███", wall_attr)
            else:
                safe_addstr(stdscr, screen_y, screen_x + 2, "   ", 0)

            if has_wall(cell, 'W'):
                safe_addstr(stdscr, screen_y + 1, screen_x, "██", wall_attr)
            else:
                safe_addstr(stdscr, screen_y + 1, screen_x, "  ", 0)

            if x == entry_x and y == entry_y:
                safe_addstr(stdscr, screen_y + 1, screen_x + 2,
                            " E ", entry_attr)
            elif x == exit_x and y == exit_y:
                safe_addstr(stdscr, screen_y + 1, screen_x + 2,
                            " X ", entry_attr)
            elif (x, y) in maze.pattern_42:
                safe_addstr(stdscr, screen_y + 1, screen_x + 2,
                            "   ", pattern_attr)
            else:
                safe_addstr(stdscr, screen_y + 1, screen_x + 2,
                            "   ", 0)

    for y in range(maze.height):
        right_cell = maze.grid[y][maze.width - 1]

        screen_x = maze.width * CELL_WIDTH
        screen_y = y * CELL_HEIGHT

        safe_addstr(stdscr, screen_y, screen_x, "██", wall_attr)
        if has_wall(right_cell, 'E'):
            safe_addstr(stdscr, screen_y + 1, screen_x, "██", wall_attr)
        else:
            safe_addstr(stdscr, screen_y + 1, screen_x, "  ", 0)

    for x in range(maze.width):
        bottom_cell = maze.grid[maze.height - 1][x]

        screen_x = x * CELL_WIDTH
        screen_y = maze.height * CELL_HEIGHT

        safe_addstr(stdscr, screen_y, screen_x, "██", wall_attr)
        if has_wall(bottom_cell, 'S'):
            safe_addstr(stdscr, screen_y, screen_x + 2, "███", wall_attr)
        else:
            safe_addstr(stdscr, screen_y, screen_x + 2, "   ", 0)

    safe_addstr(stdscr, maze.height * CELL_HEIGHT,
                maze.width * CELL_WIDTH, "██", wall_attr)


def draw_menu(stdscr: 'curses.window',
              color_index: int, pattern_index: int, maze_height: int) -> None:
    """Draw the controls menu below the maze."""
    menu_y = maze_height * CELL_HEIGHT + 2
    max_y, _ = stdscr.getmaxyx()
    if menu_y + 4 >= max_y:
        return

    color_text = COLOR_NAMES[color_index]
    pattern_text = PATTERN_COLOR_NAMES[pattern_index]

    safe_addstr(stdscr, menu_y, 0,
                "[R] Regenerate       [Q] Quit", curses.A_BOLD)
    safe_addstr(stdscr, menu_y + 1, 0,
                "[T] Change 42 Color  [C] Change Color", curses.A_BOLD)
    safe_addstr(stdscr, menu_y + 2, 0,
                "[P] Show Path        [H] Hide Path", curses.A_BOLD)
    safe_addstr(stdscr, menu_y + 3, 0,
                f"Wall: {color_text}", curses.A_BOLD)
    safe_addstr(stdscr, menu_y + 4, 0,
                f"42: {pattern_text}", curses.A_BOLD)


def draw_path(stdscr: 'curses.window', path, count: int,
              entry: Tuple[int, int], exit_pos: Tuple[int, int]) -> None:
    """Draw only the first 'count' cells of the path."""
    path_attr = curses.color_pair(10)

    for (x, y) in path[:count]:
        if (x, y) == entry or (x, y) == exit_pos:
            continue

        screen_x = x * CELL_WIDTH + 2
        screen_y = y * CELL_HEIGHT + 1

        safe_addstr(stdscr, screen_y, screen_x, "   ", path_attr)


def generate_maze(width: int, height: int, entry: Tuple[int, int],
                  exit_pos: Tuple[int, int], perfect: bool,
                  seed: int) -> MazeGenerator:
    """Generate and return a maze."""
    gen = MazeGenerator(width, height, seed, entry=entry,
                        exit=exit_pos, perfect=perfect)
    if perfect is False:
        gen.generate_imperfect_maze()
    else:
        gen.generate_perfect_maze()
    return gen


def main_loop(stdscr: 'curses.window', config: Dict[str, Any]) -> None:
    """Main loop: draw the maze and menu, wait for a key, handle it."""
    setup_colors()

    width: int = config['WIDTH']
    height: int = config['HEIGHT']
    entry: Tuple[int, int] = config['ENTRY']
    exit_pos: Tuple[int, int] = config['EXIT']
    perfect: bool = config['PERFECT']
    seed: int = config['SEED']

    maze = generate_maze(width, height, entry, exit_pos, perfect, seed)

    path = find_the_way(maze)
    show_path = False
    path_progress = 0

    color_index: int = 0
    color_list: List[int] = [1, 2, 3, 4]

    pattern_colors = [5, 7, 8, 9]
    pattern_index = 0

    while True:
        stdscr.clear()
        draw_maze(stdscr, maze, color_list[color_index],
                  pattern_colors[pattern_index])

        if show_path and path:
            draw_path(stdscr, path, path_progress, maze.entry, maze.exit)

        draw_menu(stdscr, color_index, pattern_index, maze.height)
        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('r'), ord('R')):
            seed = random.randint(1, 9999)
            maze = generate_maze(width, height, entry, exit_pos, perfect, seed)
            path = find_the_way(maze)
            show_path = False
            path_progress = 0
        elif key in (ord('c'), ord('C')):
            color_index = (color_index + 1) % len(color_list)
        elif key in (ord('t'), ord('T')):
            pattern_index = (pattern_index + 1) % len(pattern_colors)
        elif key in (ord('p'), ord('P')):
            if path and not show_path:
                show_path = True
                path_progress = 0

                for i in range(1, len(path) + 1):
                    path_progress = i
                    stdscr.clear()
                    draw_maze(stdscr, maze, color_list[color_index],
                              pattern_colors[pattern_index])
                    draw_path(stdscr, path, path_progress,
                              maze.entry, maze.exit)
                    draw_menu(stdscr, color_index, pattern_index, maze.height)
                    stdscr.refresh()
                    curses.napms(80)
        elif key in (ord('h'), ord('H')):
            show_path = False
            path_progress = 0


def run_display(config: Dict[str, Any]) -> None:
    """Entry point: start the curses visualizer."""
    try:
        curses.wrapper(lambda stdscr: main_loop(stdscr, config))
    except KeyboardInterrupt:
        pass
