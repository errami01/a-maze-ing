from typing import List, Tuple


class TerminalRenderer:
    """Render maze in terminal with optional path and colors."""

    COLORS = [
        "\033[97m",  # white
        "\033[92m",  # green
        "\033[94m",  # blue
        "\033[93m",  # yellow
        "\033[91m",  # red
    ]

    RESET = "\033[0m"

    def __init__(self) -> None:
        self.show_path = False
        self.color_index = 0

    def next_color(self) -> None:
        """Change wall color."""
        self.color_index = (self.color_index + 1) % len(self.COLORS)

    def render(
        self,
        maze,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        path: str | None = None,
    ) -> None:

        height = len(maze)
        width = len(maze[0])

        path_cells = set()

        if self.show_path and path:
            x, y = entry

            for move in path:
                path_cells.add((x, y))

                if move == "N":
                    y -= 1
                elif move == "E":
                    x += 1
                elif move == "S":
                    y += 1
                elif move == "W":
                    x -= 1

            path_cells.add(exit)

        color = self.COLORS[self.color_index]

        print()

        # Top border
        print(color + "+" + "---+" * width + self.RESET)

        for y in range(height):

            line1 = color + "|" + self.RESET
            line2 = color + "+" + self.RESET

            for x in range(width):

                cell = maze[y][x]

                char = " "

                if (x, y) == entry:
                    char = "E"
                elif (x, y) == exit:
                    char = "X"
                elif (x, y) in path_cells:
                    char = "*"

                line1 += f" {char} "

                if cell.east:
                    line1 += color + "|" + self.RESET
                else:
                    line1 += " "

                if cell.south:
                    line2 += color + "---+" + self.RESET
                else:
                    line2 += "   +"

            print(line1)
            print(line2)
