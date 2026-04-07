import sys
from file_IO_sanitization import read_file
from class_generator import MazeGenerator
from hexadicimal_encoder import encode_and_export_maze
from visualizing_maze import MazeVisualizer


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # 1. Parse configuration
        config = read_file(config_file)

        # 2. Generate the maze (Teammate's class)
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_pos=config.exit,
            perfect=config.perfect,
        )
        shortest_path = generator.solve()

        # 3. Encode and export to file
        encode_and_export_maze(
            maze_grid=generator.grid,
            entry=config.entry,
            exit_coords=config.exit,
            shortest_path=shortest_path,
            output_file=config.output_file,
        )

        # 4. Launch the visualizer
        visualizer = MazeVisualizer(
            maze_grid=generator.grid, shortest_path=shortest_path, config=config
        )
        visualizer.interaction_loop()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("unexcepected error!!!!")
