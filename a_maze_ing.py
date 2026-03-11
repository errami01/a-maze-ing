from src.mazegen.maze_generator import MazeGenerator
from maze.renderer import TerminalRenderer
from maze.config_parser import parse_config
import sys

def render_ascii(maze):
    """Display maze in ASCII."""
    height = len(maze)
    width = len(maze[0])

    # Top border
    print("+" + "---+" * width)

    for y in range(height):
        line1 = "|"
        line2 = "+"

        for x in range(width):
            cell = maze[y][x]

            # floor
            line1 += "   "

            if cell.east:
                line1 += "|"
            else:
                line1 += " "

            if cell.south:
                line2 += "---+"
            else:
                line2 += "   +"

        print(line1)
        print(line2)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:

        config = parse_config(config_file)
        entry = config["entry"]
        exit = config["exit"]
        generator = MazeGenerator(
            width=config["width"],
            height=config["height"],
            seed=config["seed"],
            entry=config["entry"],
            exit=config["exit"],
            perfect=config["perfect"],
            # algorithm=config["algorithm"]
        )

        generator.generate()

        maze = generator.grid
        path = generator.solve()
        print(maze[8][13])
        print(maze[6][12])
        generator.export(config["output"],entry, exit, path)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # generator = MazeGenerator(width, height, seed=42, perfect=False)

    renderer = TerminalRenderer()

    # generator.generate()
    # maze = generator.grid
    # path = generator.solve(entry, exit)
    
    while True:

        renderer.render(maze, entry, exit, path)

        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide from the entrance to the exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        command = input("Choice (1-4): ").strip()

        if command == "4":
            break

        elif command == "2":
            renderer.show_path = not renderer.show_path

        elif command == "3":
            renderer.next_color()

        elif command == "1":
            generator.generate()
            maze = generator.grid
            path = generator.solve()
            print(maze[8][13])
            print(maze[6][12])
            generator.export(config["output"],entry, exit, path)

if __name__ == "__main__":
    main()
