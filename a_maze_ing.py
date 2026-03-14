from logging import config
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
    with open(filename, 'w') as f:
        # Write maze in hexadecimal
        for row in maze:
            f.write(''.join(format(cell, '') for cell in row) + '\n')
        f.write('\n')
        # Write entry coordinates
        f.write(f"{maze.entry}\n")
        # Write exit coordinates
        f.write(f"{maze.exit}\n")
        # Write solution path
        f.write("".join(move for move in path) + "\n")
        


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
            maze = generator.generate_perfect_maze()
        else:
            maze = generator.generate_imperfect_maze()

        path = find_the_way(maze, config["ENTRY"], config["EXIT"])
        write_output_file(config["OUTPUT_FILE"], generator, path)
        run_display(config, generator)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
