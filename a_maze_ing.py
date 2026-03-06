import sys
from typing import Any

from Visualisation.configparsing import parse_config
from Algo.generator import MazeGenerator
from Visualisation.display import run_display


def build_generator(config: dict[str, Any]) -> MazeGenerator:
    """Create and return the maze generator from parsed config."""
    perfect = config["PERFECT"]

    return MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        perfect=perfect,
    )


def main() -> None:
    """Program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config = parse_config(config_path)
        generator = build_generator(config)
        maze = generator.generate(config["ENTRY"], config["EXIT"])
        generator.save_to_file(maze, config["OUTPUT_FILE"])
        run_display(maze, config, generator)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
