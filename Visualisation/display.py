import curses
import random
import time
from typing import List, Tuple, Dict, Any
from mazegen.generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.solver import solve_this_maze
from src.validator import is_42_cell


COLOR_NAMES: List[str] = ["White", "Green", "Red", "Blue"]

DIRECTION_OFFSETS: Dict[str, Tuple[int, int]] = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}


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
    """Write text at position (y, x). Do nothing if out of bounds.
    param stdscr: Curses window to write to.
    param y: Y-coordinate to write at.
    param x: X-coordinate to write at.
    param text: Text to write.
    param attr: Curses attribute for the text."""
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x < 0 or x + len(text) >= max_x:
        return
    stdscr.addstr(y, x, text, attr)


def draw_maze(stdscr: 'curses.window', maze: Maze,
              wall_color: int) -> None:
    """Draw the maze walls and cell contents on screen.
    param stdscr: Curses window to draw on.
    param maze: Maze object to be drawn.
    param wall_color: Color pair index for the walls."""
    wall_attr = curses.color_pair(wall_color)
    pattern_attr = curses.color_pair(7)
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
            color = pattern_attr if is_42_cell(cell) else wall_attr

            safe_addstr(stdscr, screen_y, screen_x, "█", color)

            if cell.has_wall('N'):
                safe_addstr(stdscr, screen_y, screen_x + 1, "███", color)
            else:
                safe_addstr(stdscr, screen_y, screen_x + 1, "   ", color)

            if cell.has_wall('W'):
                safe_addstr(stdscr, screen_y + 1, screen_x, "█", color)
            else:
                safe_addstr(stdscr, screen_y + 1, screen_x, " ", color)

            if x == entry_x and y == entry_y:
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            " E ", entry_attr)
            elif x == exit_x and y == exit_y:
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            " X ", entry_attr)
            elif is_42_cell(cell):
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            "42", pattern_attr)
            else:
                safe_addstr(stdscr, screen_y + 1, screen_x + 1,
                            "   ", color)

    for y in range(maze.height):
        right_cell = maze.get_cell(maze.width - 1, y)
        if not right_cell:
            continue
        screen_x = maze.width * 4
        screen_y = y * 2
        color = pattern_attr if is_42_cell(right_cell) else wall_attr
        safe_addstr(stdscr, screen_y, screen_x, "█", color)
        if right_cell.has_wall('E'):
            safe_addstr(stdscr, screen_y + 1, screen_x, "█", color)
        else:
            safe_addstr(stdscr, screen_y + 1, screen_x, " ", color)

    for x in range(maze.width):
        bottom_cell = maze.get_cell(x, maze.height - 1)
        if not bottom_cell:
            continue
        screen_x = x * 4
        screen_y = maze.height * 2
        color = pattern_attr if is_42_cell(bottom_cell) else wall_attr
        safe_addstr(stdscr, screen_y, screen_x, "█", color)
        if bottom_cell.has_wall('S'):
            safe_addstr(stdscr, screen_y, screen_x + 1, "███", color)
        else:
            safe_addstr(stdscr, screen_y, screen_x + 1, "   ", color)

    safe_addstr(stdscr, maze.height * 2, maze.width * 4, "█", wall_attr)


def draw_path(stdscr: 'curses.window', maze: Maze,
              path: List[str], entry: Tuple[int, int],
              animate: bool = False) -> None:
    """Draw the solution path over the maze with colors.
    param stdscr: Curses window to draw on.
    param maze: Maze object to be drawn.
    param path: List of directions (N, S, E, W) representing the solution path.
    param entry: Tuple of (x, y) coordinates for the entry point.
    param animate: Whether to animate the path drawing."""
    path_attr = curses.color_pair(5)
    entry_attr = curses.color_pair(8)
    exit_attr = curses.color_pair(9)

    x, y = entry
    path_cells: List[Tuple[int, int]] = [(x, y)]
    for direction in path:
        dx, dy = DIRECTION_OFFSETS[direction]
        x += dx
        y += dy
        path_cells.append((x, y))

    for cell_x, cell_y in path_cells:
        screen_x = cell_x * 4 + 1
        screen_y = cell_y * 2 + 1

        if (cell_x, cell_y) == maze.entry:
            safe_addstr(stdscr, screen_y, screen_x, " E ", entry_attr)
        elif (cell_x, cell_y) == maze.exit:
            safe_addstr(stdscr, screen_y, screen_x, " X ", exit_attr)
        else:
            safe_addstr(stdscr, screen_y, screen_x, "   ", path_attr)

        if animate:
            stdscr.refresh()
            time.sleep(0.02)


def draw_menu(stdscr: 'curses.window', show_path: bool,
              color_index: int, maze_height: int) -> None:
    """Draw the controls menu below the maze.
    param stdscr: Curses window to draw on.
    param show_path: Whether the path is currently shown.
    param color_index: Current index of the wall color.
    param maze_height: Height of the maze to position the menu correctly."""
    menu_y = maze_height * 2 + 2
    max_y, max_x = stdscr.getmaxyx()
    if menu_y + 1 >= max_y:
        return

    path_text = "ON" if show_path else "OFF"
    color_text = COLOR_NAMES[color_index]
    safe_addstr(stdscr, menu_y, 0,
                "[R] Regenerate  [P] Path  [C] Color  [Q] Quit", curses.A_BOLD)
    safe_addstr(stdscr, menu_y + 1, 0,
                f"Path: {path_text} | Color: {color_text}", curses.A_BOLD)


def main_loop(stdscr: 'curses.window', config: Dict[str, Any]) -> None:
    """Main loop: draw the maze, wait for a key, handle it, repeat.
    param stdscr: Curses window to draw on.
    param config: Dictionary of configuration values."""
    setup_colors()

    width: int = config['WIDTH']
    height: int = config['HEIGHT']
    entry: Tuple[int, int] = config['ENTRY']
    exit_pos: Tuple[int, int] = config['EXIT']
    perfect: bool = config['PERFECT']
    seed: int = random.randint(0, 999999)

    gen = MazeGenerator(width=width, height=height,
                        perfect=perfect, seed=seed)
    maze = gen.generate(entry=entry, exit=exit_pos)
    path = solve_this_maze(maze, entry, exit_pos)

    show_path: bool = False
    animate_path: bool = False
    color_index: int = 0
    color_list: List[int] = [1, 2, 3, 4]

    while True:
        stdscr.clear()
        draw_maze(stdscr, maze, color_list[color_index])
        if show_path:
            draw_path(stdscr, maze, path, entry, animate=animate_path)
            animate_path = False
        draw_menu(stdscr, show_path, color_index, maze.height)
        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('r'), ord('R')):
            seed = random.randint(0, 999999)
            gen = MazeGenerator(width=width, height=height,
                                perfect=perfect, seed=seed)
            maze = gen.generate(entry=entry, exit=exit_pos)
            path = solve_this_maze(maze, entry, exit_pos)
            show_path = False
        elif key in (ord('p'), ord('P')):
            show_path = not show_path
            if show_path:
                animate_path = True
        elif key in (ord('c'), ord('C')):
            color_index = (color_index + 1) % len(color_list)


def start_visualizer(config: Dict[str, Any]) -> None:
    """Entry point: start the curses visualizer.
    param config: Dictionary of configuration values."""
    curses.wrapper(lambda stdscr: main_loop(stdscr, config))
