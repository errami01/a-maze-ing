

def parse_config(file_path):
    MANDATORY_KEYS = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
    config = {}

    try:
        with open(file_path, "r") as f:
            for line_number, line in enumerate(f, start=1):

                line = line.strip()

                # ignore empty or comment
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid syntax at line {line_number}: {line}")

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                config[key] = value

    except FileNotFoundError:
        raise FileNotFoundError("Configuration file not found.")

    # validate mandatory keys
    missing = MANDATORY_KEYS - config.keys()

    if missing:
        raise ValueError(f"Missing configuration keys: {', '.join(missing)}")

    return validate_config(config)


def validate_config(config):

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])

        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers.")

        entry = parse_coordinates(config["ENTRY"])
        exit_ = parse_coordinates(config["EXIT"])

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("ENTRY is outside maze bounds.")

        if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
            raise ValueError("EXIT is outside maze bounds.")

        perfect = parse_bool(config["PERFECT"])

        seed = None
        if "SEED" in config:
            seed = int(config["SEED"])

        algorithm = config["ALGORITHM"]

        return {
            "width": width,
            "height": height,
            "entry": entry,
            "exit": exit_,
            "output": config["OUTPUT_FILE"],
            "perfect": perfect,
            "seed": seed,
            "algorithm": algorithm
        }

    except ValueError as e:
        raise ValueError(f"Invalid configuration: {e}")


def parse_coordinates(value):

    if "," not in value:
        raise ValueError(f"Invalid coordinate format: {value}")

    x, y = value.split(",")

    return int(x), int(y)


def parse_bool(value):

    value = value.lower()

    if value in ["true", "1", "yes"]:
        return True

    if value in ["false", "0", "no"]:
        return False

    raise ValueError(f"Invalid boolean value: {value}")
