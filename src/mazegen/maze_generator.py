from dataclasses import dataclass
from typing import List, Tuple, Optional, Literal
import random
from collections import deque


@dataclass
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True


class MazeGenerator:
    """
    Generate and solve rectangular mazes.

    Parameters:
        width (int): Maze width
        height (int): Maze height
        entry (Tuple[int, int]): Start position
        exit (Tuple[int, int]): End position
        seed (Optional[int]): Random seed
        perfect (bool): Generate perfect maze
        algorithm (str): Maze generation algorithm ("dfs" or "prim")
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = True,
        algorithm: Literal["dfs", "prim"] = "dfs",
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        self.algorithm = algorithm.lower()
        self._rng = random.Random(seed)
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]
        self.forty_two = FortyTwo(self.width, self.height)

        if self.algorithm not in {"dfs", "prim"}:
            raise ValueError("algorithm must be 'dfs' or 'prim'")

    def generate(self) -> None:
        """Generate a new maze using the selected algorithm."""

        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        if self.algorithm == "dfs":
            self._generate_dfs()
        elif self.algorithm == "prim":
            self._generate_prim()

        if not self.perfect:
            self._add_extra_connections()

        self._apply_42()

    def _generate_dfs(self) -> None:
        """Generate a new maze using DFS"""

        visited = {(0, 0)}
        stack = [(0, 0)]

        while stack:
            x, y = stack[-1]

            neighbors = self._get_unvisited_neighbors(x, y, visited)

            if not neighbors:
                stack.pop()
                continue

            self._rng.shuffle(neighbors)

            for nx, ny, direction in neighbors:
                if self._remove_wall(x, y, nx, ny, direction):
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

    def _generate_prim(self) -> None:
        """Generate a new maze using Prim"""

        blocked = set(self.forty_two.get_cells())
        start = (0, 0)

        visited = {start}
        frontier: List[Tuple[int, int, int, int, str]] = []

        self._add_frontier_edges(start[0], start[1], visited,
                                 frontier, blocked)

        while frontier:
            idx = self._rng.randrange(len(frontier))
            x, y, nx, ny, direction = frontier.pop(idx)

            if (nx, ny) in visited:
                continue

            if self._remove_wall(x, y, nx, ny, direction):
                visited.add((nx, ny))
                self._add_frontier_edges(nx, ny, visited, frontier, blocked)

    def _add_frontier_edges(
        self,
        x: int,
        y: int,
        visited: set[Tuple[int, int]],
        frontier: List[Tuple[int, int, int, int, str]],
        blocked: set[Tuple[int, int]],
    ) -> None:
        """add edges for current cell"""

        for direction, (nx, ny) in self._neighbor_coords(x, y).items():
            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in visited
                and (nx, ny) not in blocked
            ):
                frontier.append((x, y, nx, ny, direction))

    def _neighbor_coords(self, x: int, y: int) -> dict[str, Tuple[int, int]]:
        return {
            "N": (x, y - 1),
            "E": (x + 1, y),
            "S": (x, y + 1),
            "W": (x - 1, y),
        }

    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int,
        visited: set[Tuple[int, int]]
    ) -> List[Tuple[int, int, str]]:
        neighbors = []
        forty_two_cells = set(self.forty_two.get_cells())
        directions = self._neighbor_coords(x, y)

        for direction, (nx, ny) in directions.items():
            if (
                0 <= nx < self.width and
                0 <= ny < self.height and
                (nx, ny) not in visited and
                (nx, ny) not in forty_two_cells
            ):
                neighbors.append((nx, ny, direction))

        return neighbors

    def _remove_wall(
        self,
        x: int,
        y: int,
        nx: int,
        ny: int,
        direction: str
    ) -> bool:
        cell = self.grid[y][x]
        neighbor = self.grid[ny][nx]
        forty_two_cells = set(self.forty_two.get_cells())

        prev = (
            cell.north, cell.east, cell.south, cell.west,
            neighbor.north, neighbor.east, neighbor.south, neighbor.west
        )

        if direction == "N":
            cell.north = (nx, ny) in forty_two_cells
            neighbor.south = (x, y) in forty_two_cells
        elif direction == "E":
            cell.east = (nx, ny) in forty_two_cells
            neighbor.west = (x, y) in forty_two_cells
        elif direction == "S":
            cell.south = (nx, ny) in forty_two_cells
            neighbor.north = (x, y) in forty_two_cells
        elif direction == "W":
            cell.west = (nx, ny) in forty_two_cells
            neighbor.east = (x, y) in forty_two_cells

        if self._creates_3x3_open(x, y) or self._creates_3x3_open(nx, ny):
            (
                cell.north, cell.east, cell.south, cell.west,
                neighbor.north, neighbor.east, neighbor.south, neighbor.west
            ) = prev
            return False
        return True

    def _creates_3x3_open(self, x: int, y: int) -> bool:
        """Check if a 3x3 open area exists around a position."""

        for dy in range(-2, 1):
            for dx in range(-2, 1):
                cx = x + dx
                cy = y + dy

                if not (
                    0 <= cx <= self.width - 3
                    and 0 <= cy <= self.height - 3
                ):
                    continue

                if self._is_3x3_open(cx, cy):
                    return True

        return False

    def _is_3x3_open(self, x: int, y: int) -> bool:
        """Return True if the 3x3 block at (x,y) is fully open inside."""

        for j in range(3):
            for i in range(3):
                cell = self.grid[y + j][x + i]

                if i < 2 and cell.east:
                    return False

                if j < 2 and cell.south:
                    return False

        return True

    def solve(self) -> str:
        """Return shortest path as NESW string."""
        queue = deque([(self.entry, "")])
        visited = {self.entry}

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == self.exit:
                return path

            for dx, dy, d in [
                (0, -1, "N"),
                (1, 0, "E"),
                (0, 1, "S"),
                (-1, 0, "W"),
            ]:
                nx, ny = x + dx, y + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue

                if (nx, ny) in visited:
                    continue

                if self._can_move(x, y, d):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + d))

        raise ValueError("No path found")

    def _can_move(self, x: int, y: int, direction: str) -> bool:
        cell = self.grid[y][x]
        return not getattr(cell, {
            "N": "north",
            "E": "east",
            "S": "south",
            "W": "west",
        }[direction])

    def to_hex_rows(self) -> List[str]:
        """Return maze as list of hex-encoded rows."""
        rows = []
        for row in self.grid:
            hex_row = ""
            for cell in row:
                value = (
                    (cell.north << 0) |
                    (cell.east << 1) |
                    (cell.south << 2) |
                    (cell.west << 3)
                )
                hex_row += format(value, "X")
            rows.append(hex_row)
        return rows

    def export(
        self,
        file_path: str,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        solution: str
    ) -> None:
        """Write maze to output file."""

        rows = self.to_hex_rows()

        with open(file_path, "w") as f:
            for row in rows:
                f.write(row + "\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_[0]},{exit_[1]}\n")
            f.write(solution + "\n")

    def _add_extra_connections(self) -> None:
        """Add extra connections without creating 3x3 areas."""

        attempts = (self.width * self.height) // 5

        for _ in range(attempts):
            x = self._rng.randrange(self.width)
            y = self._rng.randrange(self.height)

            direction = self._rng.choice(["N", "E", "S", "W"])

            dx, dy = {
                "N": (0, -1),
                "E": (1, 0),
                "S": (0, 1),
                "W": (-1, 0),
            }[direction]

            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                self._remove_wall(x, y, nx, ny, direction)

    def _apply_42(self) -> None:
        closed_cells = self.forty_two.get_cells()

        for (x, y) in closed_cells:
            cell = self.grid[y][x]
            cell.north = True
            cell.south = True
            cell.east = True
            cell.west = True


class FortyTwo:
    """
    Set the coordinates for the Forty Two pattern
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.x = int((width / 2) - 3)
        self.y = int((height / 2) - 2)

    def get_cells(self) -> List[Tuple[int, int]]:
        if self.width < 14 or self.height < 10:
            return []

        four = [
            (self.x, self.y),
            (self.x, self.y + 1),
            (self.x, self.y + 2),
            (self.x + 1, self.y + 2),
            (self.x + 2, self.y + 2),
            (self.x + 2, self.y + 3),
            (self.x + 2, self.y + 4),
        ]

        two = [
            (self.x + 4, self.y),
            (self.x + 5, self.y),
            (self.x + 6, self.y),
            (self.x + 6, self.y + 1),
            (self.x + 6, self.y + 2),
            (self.x + 5, self.y + 2),
            (self.x + 4, self.y + 2),
            (self.x + 4, self.y + 3),
            (self.x + 4, self.y + 4),
            (self.x + 5, self.y + 4),
            (self.x + 6, self.y + 4),
        ]

        return four + two
