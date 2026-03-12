import sys
from typing import Any

from visualisation.parsing import parse_config
from mazegen.generator import MazeGenerator
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

        run_display(config, generator)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
