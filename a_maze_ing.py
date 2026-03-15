import sys
from typing import Any

from visualisation.parsing import parse_config
from mazegen.generator import MazeGenerator
from mazegen.show_the_exit import find_the_way
from visualisation.display import run_display


def build_generator(config: dict[str, Any]) -> MazeGenerator:
    """Create and return the maze generator from parsed config."""
    return MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        config["SEED"],
        entry=config["ENTRY"],
        exit=config["EXIT"],
        perfect=config["PERFECT"],
    )


def path_to_directions(path: list[tuple[int, int]]) -> str:
    """Convert a coordinate path into N/E/S/W directions."""
    directions = []

    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]

        if curr_x == prev_x and curr_y == prev_y - 1:
            directions.append("N")
        elif curr_x == prev_x + 1 and curr_y == prev_y:
            directions.append("E")
        elif curr_x == prev_x and curr_y == prev_y + 1:
            directions.append("S")
        elif curr_x == prev_x - 1 and curr_y == prev_y:
            directions.append("W")

    return "".join(directions)


def write_output_file(filename: str, maze: MazeGenerator,
                      path: list[tuple[int, int]]) -> None:
    """Write the maze and path in hexadecimal to a text file.
    Args:
            maze: Maze to save
            filename: Output filename

        File format:
            - One hex digit per cell (walls encoding)
            - One row per line
            - Empty line
            - Entry coordinates
            - Exit coordinates
            - Solution path (N, E, S, W moves)
    """
    path_string = path_to_directions(path)
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    with open(filename, "w", encoding="utf-8") as file:
        for row in maze.grid:
            hex_row = "".join(format(cell, "X") for cell in row)
            file.write(hex_row + "\n")

        file.write("\n")
        file.write(f"{entry_x},{entry_y}\n")
        file.write(f"{exit_x},{exit_y}\n")
        file.write(path_string + "\n")


def main() -> None:
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config = parse_config(config_path)
        generator = build_generator(config)

        if config["PERFECT"]:
            generator.generate_perfect_maze()
        else:
            generator.generate_imperfect_maze()

        path = find_the_way(generator)
        if path is None:
            raise RuntimeError("No path found from entry to exit")
        if "OUTPUT_FILE" in config and config["OUTPUT_FILE"]:
            write_output_file(config["OUTPUT_FILE"], generator, path)

        run_display(config, generator)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
