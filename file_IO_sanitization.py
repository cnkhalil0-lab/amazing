import sys
from typing import Dict, Tuple, Set
from dataclasses import dataclass


@dataclass
class NecessaryVariables:
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool


def read_file(file_name: str) -> NecessaryVariables:
    variables_needed: Dict[str, str] = {}
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            for count, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"In line '{line}' there is no equal symbol '='")
                key, value = line.split("=", 1)
                variables_needed[key.strip()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"There is no file named {file_name}, enter an existing file"
        )
    except PermissionError:
        raise PermissionError(f"Permission denied, you can't read from {file_name}")
    except IsADirectoryError:
        raise IsADirectoryError(f"{file_name} is a directory not a file")
    except ValueError as e:
        raise e

    mandatory_variables: Set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
    missing_ones: Set[str] = mandatory_variables - variables_needed.keys()
    if missing_ones:
        raise ValueError(
            f"You are missing the following mandatory variables: {missing_ones}"
        )

    try:
        width = int(variables_needed["WIDTH"])
    except ValueError:
        raise ValueError("Invalid width, it contains non-digit characters")
    if width <= 0:
        raise ValueError("Width must be a positive integer")

    try:
        height = int(variables_needed["HEIGHT"])
    except ValueError:
        raise ValueError("Invalid height, it contains non-digit characters")
    if height <= 0:
        raise ValueError("Height must be a positive integer")

    x_str, y_str = variables_needed["ENTRY"].split(",", 1)
    try:
        entry = (int(x_str.strip()), int(y_str.strip()))
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Entry is out of bounds")
    except ValueError:
        raise ValueError("Invalid entry or out of bounds")

    x_str, y_str = variables_needed["EXIT"].split(",", 1)
    try:
        exit_pos: Tuple[int, int] = (int(x_str.strip()), int(y_str.strip()))
        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            raise ValueError("Exit is out of bounds")
    except ValueError:
        raise ValueError("Invalid exit or out of bounds")

    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT cannot be the same.")

    output_file: str = variables_needed["OUTPUT_FILE"].strip()

    if variables_needed["PERFECT"] not in ("True", "False", "0", "1"):
        raise ValueError("PERFECT must be a boolean")
    else:
        perfect = variables_needed["PERFECT"] in ("True", "1")

    return NecessaryVariables(
        width=width,
        height=height,
        entry=entry,
        exit=exit_pos,
        output_file=output_file,
        perfect=perfect,
    )
