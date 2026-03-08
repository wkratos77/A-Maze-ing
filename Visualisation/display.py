import curses
import random
from typing import List, Tuple, Dict, Any
from Algo.generator import MazeGenerator


COLOR_NAMES: List[str] = ["White", "Green", "Red", "Blue"]


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
    curses.init_pair(7, curses.COLOR_CYAN, -1)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)


def safe_addstr(stdscr: 'curses.window', y: int, x: int,
                text: str, attr: int) -> None:
    """Write text at position (y, x). Do nothing if out of bounds."""
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x < 0 or x + len(text) > max_x:
        return
    stdscr.addstr(y, x, text, attr)


def draw_maze(stdscr: 'curses.window', maze: Maze,
              wall_color: int) -> None:
    """Draw the maze walls and cell contents on screen."""
    wall_attr = curses.color_pair(wall_color)
    entry_attr = curses.color_pair(6) | curses.A_BOLD
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            if not cell:
                continue

            screen_x = x * 4
            screen_y = y * 2

            safe_addstr(stdscr, screen_y, screen_x, "█", wall_attr)

            if cell.has_wall('N'):
                safe_addstr(stdscr, screen_y, screen_x + 1, "███", wall_attr)
            else:
                safe_addstr(stdscr, screen_y, screen_x + 1, "   ", 0)

            if cell.has_wall('W'):
                safe_addstr(stdscr, screen_y + 1, screen_x, "█", wall_attr)
            else:
                safe_addstr(stdscr, screen_y + 1, screen_x, " ", 0)

            if x == entry_x and y == entry_y:
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            " E ", entry_attr)
            elif x == exit_x and y == exit_y:
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            " X ", entry_attr)
            else:
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            "   ", 0)

    for y in range(maze.height):
        right_cell = maze.get_cell(maze.width - 1, y)
        if not right_cell:
            continue

        screen_x = maze.width * 4
        screen_y = y * 2

        safe_addstr(stdscr, screen_y, screen_x, "█", wall_attr)
        if right_cell.has_wall('E'):
            safe_addstr(stdscr, screen_y + 1, screen_x, "█", wall_attr)
        else:
            safe_addstr(stdscr, screen_y + 1, screen_x, " ", 0)

    for x in range(maze.width):
        bottom_cell = maze.get_cell(x, maze.height - 1)
        if not bottom_cell:
            continue

        screen_x = x * 4
        screen_y = maze.height * 2

        safe_addstr(stdscr, screen_y, screen_x, "█", wall_attr)
        if bottom_cell.has_wall('S'):
            safe_addstr(stdscr, screen_y, screen_x + 1, "███", wall_attr)
        else:
            safe_addstr(stdscr, screen_y, screen_x + 1, "   ", 0)

    safe_addstr(stdscr, maze.height * 2, maze.width * 4, "█", wall_attr)


def draw_menu(stdscr: 'curses.window',
              color_index: int, maze_height: int) -> None:
    """Draw the controls menu below the maze."""
    menu_y = maze_height * 2 + 2
    max_y, _ = stdscr.getmaxyx()
    if menu_y + 1 >= max_y:
        return

    color_text = COLOR_NAMES[color_index]

    safe_addstr(stdscr, menu_y, 0,
                "[R] Regenerate  [C] Color  [Q] Quit", curses.A_BOLD)
    safe_addstr(stdscr, menu_y + 1, 0,
                f"Color: {color_text}", curses.A_BOLD)


def generate_maze(width: int, height: int, entry: Tuple[int, int],
                  exit_pos: Tuple[int, int], perfect: bool,
                  seed: int) -> Maze:
    """Generate and return a maze."""
    gen = MazeGenerator(width=width, height=height,
                        perfect=perfect, seed=seed)
    return gen.generate(entry=entry, exit=exit_pos)


def main_loop(stdscr: 'curses.window', config: Dict[str, Any]) -> None:
    """Main loop: draw the maze and menu, wait for a key,
    either C or Q or P or R, handle it, repeat."""
    setup_colors()

    width: int = config['WIDTH']
    height: int = config['HEIGHT']
    entry: Tuple[int, int] = config['ENTRY']
    exit_pos: Tuple[int, int] = config['EXIT']
    perfect: bool = config['PERFECT']
    seed: int = config['SEED']

    maze = generate_maze(width, height, entry, exit_pos, perfect, seed)

    color_index: int = 0
    color_list: List[int] = [1, 2, 3, 4]

    while True:
        stdscr.clear()
        draw_maze(stdscr, maze, color_list[color_index])
        draw_menu(stdscr, color_index, maze.height)
        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('r'), ord('R')):
            seed = random.randint(1, 9999)
            maze = generate_maze(width, height, entry, exit_pos, perfect, seed)
        elif key in (ord('c'), ord('C')):
            color_index = (color_index + 1) % len(color_list)


def run_display(config: Dict[str, Any]) -> None:
    """Entry point: start the curses visualizer."""
    curses.wrapper(lambda stdscr: main_loop(stdscr, config))
