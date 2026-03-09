import sys
from typing import Any


def buffread(filepath: str) -> list[str]:
    """Reads the config and returns a list of lines, or exits on error."""
    read = []
    try:
        with open(filepath, 'r') as fd:
            read = fd.read().splitlines()
    except FileNotFoundError:
        print(f"Error: file '{filepath}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied for '{filepath}'.")
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: '{filepath}' is a directory, not a file.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: file '{filepath}' is not a valid text file.")
        sys.exit(1)
    except OSError as e:
        print(f"Error while reading '{filepath}': {e}")
        sys.exit(1)
    if len(read) == 0:
        print("File is empty.")
        sys.exit(1)
    return read


def get_lines(lines: list[str]) -> list[str]:
    """Takes raw lines from the file and returns
    only the meaningful ones, removing"""
    clean = []
    for line in lines:
        if line.strip().startswith('#'):
            continue
        if line.strip() == '':
            continue
        clean.append(line.strip())
    if not clean:
        print("Error: configuration file contains no valid lines.")
        sys.exit(1)
    return clean


def get_key_value(line: str) -> dict[str, str]:
    """Takes a line and returns a dict
    with the key and value, or exits on error."""
    if '=' not in line:
        print(f"Line '{line}' is not in the format 'key=value'.")
        sys.exit(1)
    key, value = line.split('=', 1)
    key = key.strip()
    value = value.strip()

    if key == "" or value == "":
        print(f"Error: invalid line '{line}'.")
        sys.exit(1)
    return {key: value}


def convert_width_height(config: dict) -> None:
    """Converts WIDTH and HEIGHT to integers, validating them,
    or exits on error."""
    for key in ("WIDTH", "HEIGHT"):
        raw = config.get(key)
        if raw is None:
            print(f"Error: Missing key {key}")
            sys.exit(1)

        try:
            val = int(raw)
        except ValueError:
            print(f"Error: {key} must be an integer (got '{raw}')")
            sys.exit(1)
        if val <= 0:
            print(f"Error: {key} must be > 0 (got {val})")
            sys.exit(1)
        config[key] = val


def convert_entry_exit(config: dict) -> None:
    """Converts ENTRY and EXIT to (x, y) tuples, validating them,
    or exits on error."""
    width = config.get("WIDTH")
    height = config.get("HEIGHT")
    if not isinstance(width, int) or not isinstance(height, int):
        print("Error: WIDTH and HEIGHT must be converted before ENTRY/EXIT")
        sys.exit(1)

    for key in ("ENTRY", "EXIT"):
        raw = config.get(key)
        if raw is None:
            print(f"Error: Missing key {key}")
            sys.exit(1)

        try:
            parts = raw.split(",")
            if len(parts) != 2:
                raise ValueError

            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError:
            print(
                f"Error: {key} must be in format 'x,y' with int (got '{raw}')"
                )
            sys.exit(1)

        if x < 0 or x >= width or y < 0 or y >= height:
            print(
                f"Error: {key} out of bounds (got {x},{y}) "
                f"for WIDTH={width}, HEIGHT={height}"
            )
            sys.exit(1)

        config[key] = (x, y)

    if config["ENTRY"] == config["EXIT"]:
        print(
            f"Error: ENTRY and EXIT must be different "
            f"(both are {config['ENTRY']})"
            )
        sys.exit(1)


def convert_output_file(config: dict[str, Any]) -> None:
    """Validate OUTPUT_FILE."""
    raw = config.get("OUTPUT_FILE")
    if raw is None:
        print("Error: missing key OUTPUT_FILE.")
        sys.exit(1)

    if not isinstance(raw, str) or raw.strip() == "":
        print("Error: OUTPUT_FILE must be a non-empty string.")
        sys.exit(1)

    config["OUTPUT_FILE"] = raw.strip()


def convert_perfect(config: dict[str, Any]) -> None:
    """Convert PERFECT to bool."""
    raw = config.get("PERFECT")
    if raw is None:
        print("Error: missing key PERFECT.")
        sys.exit(1)

    if not isinstance(raw, str):
        print("Error: PERFECT must be a string before conversion.")
        sys.exit(1)

    lowered = raw.strip().lower()
    if lowered == "true":
        config["PERFECT"] = True
    elif lowered == "false":
        config["PERFECT"] = False
    else:
        print("Error: PERFECT must be True or False.")
        sys.exit(1)


def convert_seed(config: dict[str, Any]) -> None:
    """Convert optional SEED to int."""
    raw = config["SEED"]
    if raw is None:
        print("Error: missing key SEED.")
        sys.exit(1)
    try:
        config["SEED"] = int(raw)
    except ValueError:
        print(f"Error: SEED must be an integer (got '{raw}').")
        sys.exit(1)


def parse_config(filepath: str) -> dict[str, Any]:
    """Reads the config file, validates it, and returns a dict
    with the config values."""
    buff = buffread(filepath)
    lines = get_lines(buff)
    config = {}
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"]
    for line in lines:
        kv = get_key_value(line)
        k = next(iter(kv))
        if k in config:
            print(f"Error: Duplicate key {k}")
            sys.exit(1)
        if k not in required:
            print(f"Error: Unknown key {k}")
            sys.exit(1)
        config.update(kv)
    for key in required:
        if key not in config:
            print(f"Error: Missing mandatory key {key}")
            sys.exit(1)

    convert_width_height(config)
    convert_entry_exit(config)
    convert_output_file(config)
    convert_perfect(config)
    convert_seed(config)

    return config
