from typing import List, Tuple


def encode_and_export_maze(
    maze_grid: List[List[int]],
    entry: Tuple[int, int],
    exit_coords: Tuple[int, int],
    shortest_path: str,
    output_file: str,
) -> None:
    height = len(maze_grid)
    width = len(maze_grid[0]) if height > 0 else 0
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for y in range(height):
                encode_list: List[str] = []
                for x in range(width):
                    # The generator already provides an int between 0 and 15
                    cell_value = maze_grid[y][x]
                    # Format as uppercase Hexadecimal
                    encode_list.append(f"{cell_value:X}")
                f.write("".join(encode_list) + "\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
            f.write(f"{shortest_path}\n")

    except PermissionError:
        raise PermissionError(f"Permission denied, you can't write in {output_file}")
    except IsADirectoryError:
        raise IsADirectoryError(f"{output_file} is a directory not a file")
