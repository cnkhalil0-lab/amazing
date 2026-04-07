from typing import List, Tuple, Set
from class_generator.class_generator import MazeGenerator
from file_IO_sanitization import NecessaryVariables

COLORS = {
    "RESET": "\033[0m",
    "WALL_WHITE": "\033[97m",
    "WALL_BLUE": "\033[94m",
    "WALL_GREEN": "\033[92m",
    "PATH": "\033[93m",
    "ENTRY": "\033[96m",
    "EXIT": "\033[91m",
}


class MazeVisualizer:
    def __init__(
        self, maze_grid: List[List[int]], shortest_path: str, config: NecessaryVariables
    ):
        self.config = config
        self.original_entry = config.entry
        self.original_exit = config.exit
        self.shortest_path = shortest_path

        self.show_path = False
        self.wall_colors = ["WALL_WHITE", "WALL_BLUE", "WALL_GREEN"]
        self.current_color_idx = 0

        self.maze_grid = self._inflate_grid(maze_grid)
        self.path_coords: Set[Tuple[int, int]] = self._calculate_path_coords()

    def _inflate_grid(self, dense_grid: List[List[int]]) -> List[List[int]]:
        height = len(dense_grid)
        width = len(dense_grid[0]) if height > 0 else 0
        inflated = [[0 for _ in range(width * 3)] for _ in range(height * 3)]

        for y in range(height):
            for x in range(width):
                cell_val = dense_grid[y][x]
                iy, ix = y * 3, x * 3

                # Corners are always walls
                inflated[iy][ix] = 1
                inflated[iy][ix + 2] = 1
                inflated[iy + 2][ix] = 1
                inflated[iy + 2][ix + 2] = 1

                # Edges based on bitwise flags
                inflated[iy][ix + 1] = 1 if (cell_val & 1) != 0 else 0  # North
                inflated[iy + 1][ix + 2] = 1 if (cell_val & 2) != 0 else 0  # East
                inflated[iy + 2][ix + 1] = 1 if (cell_val & 4) != 0 else 0  # South
                inflated[iy + 1][ix] = 1 if (cell_val & 8) != 0 else 0  # West

        return inflated

    def _calculate_path_coords(self) -> Set[Tuple[int, int]]:
        coords: Set[Tuple[int, int]] = set()
        # Scale original coordinates to the center of the 3x3 block
        x = self.original_entry[0] * 3 + 1
        y = self.original_entry[1] * 3 + 1
        coords.add((x, y))

        for move in self.shortest_path:
            if move == "N":
                coords.update([(x, y - 1), (x, y - 2), (x, y - 3)])
                y -= 3
            elif move == "S":
                coords.update([(x, y + 1), (x, y + 2), (x, y + 3)])
                y += 3
            elif move == "E":
                coords.update([(x + 1, y), (x + 2, y), (x + 3, y)])
                x += 3
            elif move == "W":
                coords.update([(x - 1, y), (x - 2, y), (x - 3, y)])
                x -= 3
        return coords

    def draw_maze(self) -> None:
        height = len(self.maze_grid)
        width = len(self.maze_grid[0]) if height > 0 else 0
        wall_color = COLORS[self.wall_colors[self.current_color_idx]]

        # Inflated coordinates for Entry and Exit
        entry_inflated = (
            self.original_entry[0] * 3 + 1,
            self.original_entry[1] * 3 + 1,
        )
        exit_inflated = (self.original_exit[0] * 3 + 1, self.original_exit[1] * 3 + 1)

        print("\033[H\033[J", end="")
        print(f"{COLORS['ENTRY']}A-Maze-ing======{COLORS['RESET']}\n")

        for y in range(height):
            row_str = ""
            for x in range(width):
                current_coord = (x, y)

                if current_coord == entry_inflated:
                    row_str += f"{COLORS['ENTRY']}EE{COLORS['RESET']}"
                elif current_coord == exit_inflated:
                    row_str += f"{COLORS['EXIT']}XX{COLORS['RESET']}"
                elif self.show_path and current_coord in self.path_coords:
                    row_str += f"{COLORS['PATH']}••{COLORS['RESET']}"
                elif self.maze_grid[y][x] == 1:
                    row_str += f"{wall_color}██{COLORS['RESET']}"
                else:
                    row_str += "  "
            print(row_str)
        print()

    def interaction_loop(self) -> None:
        while True:
            self.draw_maze()
            print("1. Re-generate a new maze")
            print(
                f"2. Show/Hide path from entry to exit (Currently: {'Shown' if self.show_path else 'Hidden'})"
            )
            print("3. Rotate maze colors")
            print("4. Quit")

            choice = input("\nChoice? (1-4): ").strip()

            if choice == "1":
                print("\nRebuilding the maze...")
                new_maze = MazeGenerator(
                    self.config.width,
                    self.config.height,
                    self.original_entry,
                    self.original_exit,
                    self.config.perfect,
                )
                self.shortest_path = new_maze.solve()
                self.maze_grid = self._inflate_grid(new_maze.grid)
                self.path_coords = self._calculate_path_coords()
            elif choice == "2":
                self.show_path = not self.show_path
            elif choice == "3":
                self.current_color_idx = (self.current_color_idx + 1) % len(
                    self.wall_colors
                )
            elif choice == "4":
                print("Exiting visualizer...")
                break
            else:
                print("Invalid choice, please select 1-4.")
