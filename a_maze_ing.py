from mazegen.maze_generator import MazeGenerator
from maze.renderer import TerminalRenderer



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

    width = 20
    height = 10

    entry = (0, 0)
    exit = (width - 1, height - 1)

    generator = MazeGenerator(width, height, seed=42, perfect=True)

    renderer = TerminalRenderer()

    while True:

        generator.generate()

        maze = generator.grid

        path = generator.solve(entry, exit)

        renderer.render(maze, entry, exit, path)

        print("\nCommands:")
        print(" r → regenerate maze")
        print(" p → toggle path")
        print(" c → change wall color")
        print(" q → quit")

        command = input("\nCommand: ").strip()

        if command == "q":
            break

        elif command == "p":
            renderer.show_path = not renderer.show_path

        elif command == "c":
            renderer.next_color()

        elif command == "r":
            continue

if __name__ == "__main__":
    main()
