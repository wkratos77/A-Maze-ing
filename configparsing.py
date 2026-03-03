import sys


def buffread(filepath: str) -> list[str]:
    read = []
    try:
        with open(filepath, 'r') as fd:
            read = fd.read().splitlines()
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        sys.exit(1)
    if len(read) == 0:
        print("File is empty.")
        sys.exit(1)
    return read


def get_lines(lines: list[str]) -> list[str]:
    lines = []
    for line in lines:
        if line.strip().startswith('#'):
            continue
        if line.strip() == '':
            continue
    lines.append(line.strip())
    return lines


def get_key_value(line: str) -> dict[str, str]:
    if '=' not in line:
        print(f"Line '{line}' is not in the format 'key=value'.")
        sys.exit(1)
    key, value = line.split('=', 1)
    return {key.strip(): value.strip()}


def validate_convert(config: dict[str, str]) -> dict[str, any]:
    validated = {}
    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                 'OUTPUT_FILE', 'PERFECT']
    for key, value in config.items():
        if key not in mandatory:
            print(f"Unknown configuration key: {key}")
            sys.exit(1)
        if key in ['WIDTH', 'HEIGHT']:
            try:
                validated[key] = int(value)
            except ValueError:
                print(f"Value for {key} must be an integer.")
                sys.exit(1)
                if validated[key] <= 0:
                    print(f"Value for {key} must be a positive integer.")
                    sys.exit(1)
        elif key in ['ENTRY', 'EXIT']:
            if ',' not in value:
                print(f"Value for {key} must be in the format 'x,y'.")
                sys.exit(1)
            x, y = map(int, value.split(','))
            try:
                x = int(x)
                y = int(y)
                if x < 0 or y < 0:
                    print(f"Coordinates for {key} must be non-negative.")
                    sys.exit(1)
                validated[key] = (x, y)
            except ValueError:
                print(f"Value for {key} must be integers.")
                sys.exit(1)
        elif key == 'PERFECT':
            if value.lower() in ['true', 'false']:
                validated[key] = value.lower() == 'true'
            else:
                print("Value for PERFECT must be 'true' or 'false'.")
                sys.exit(1)
        else:
            if value == '':
                print(f"Value for {key} cannot be empty.")
                sys.exit(1)
            validated[key] = value
    for m in mandatory:
        if m not in list(validated.keys()):
            print(f"Missing mandatory configuration key '{m}'.")
            sys.exit(1)
    width = validated['WIDTH']
    height = validated['HEIGHT']
    entry = validated['ENTRY']
    exit_ = validated['EXIT']
    if entry[0] < 0 or entry[0] >= width or entry[1] < 0 or entry[1] >= height:
        print(f"ENTRY {entry} is out of maze bounds ({width}x{height}).")
        sys.exit(1)
    if exit_[0] < 0 or exit_[0] >= width or exit_[1] < 0 or exit_[1] >= height:
        print(f"EXIT {exit_} is out of maze bounds ({width}x{height}).")
        sys.exit(1)
    if entry == exit_:
        print(f"ENTRY and EXIT must be different. Both are {entry}.")
        sys.exit(1)
    return validated


def parse_config(filepath: str) -> dict[str, any]:
    buff = buffread(filepath)
    lines = get_lines(buff)
    config = {}
    for line in lines:
        kv = get_key_value(line)
        if kv is not None:
            config.update(kv)
    validated_config = validate_convert(config)
    return validated_config
