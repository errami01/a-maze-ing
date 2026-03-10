"""
Reusable Maze Generator Module
"""

# from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
from collections import deque
from maze.forty_two import FortyTwo
import time


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
        seed (Optional[int]): Random seed
        perfect (bool): Generate perfect maze
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self._rng = random.Random(seed)
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]
        self.forty_two = FortyTwo(self.width, self.height)

    def generate(self) -> None:
        """Generate a new maze."""

        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]
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

        if not self.perfect:
            self._add_extra_connections()
        self._apply_42()


    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int,
        visited: set[Tuple[int, int]]
    ) -> List[Tuple[int, int, str]]:
        neighbors = []
        forty_two_cells = self.forty_two.get_cells()
        directions = {
            "N": (x, y - 1),
            "E": (x + 1, y),
            "S": (x, y + 1),
            "W": (x - 1, y),
        }

        for direction, (nx, ny) in directions.items():
            if (
                0 <= nx < self.width and
                0 <= ny < self.height and
                (nx, ny) not in visited and
                (nx, ny) not in  forty_two_cells
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
        # forty_two_cells = self.forty_two.get_cells()
        # if (ny, nx) in forty_two_cells or (y, x) in forty_two_cells:
        #     return False
        #befor removing
        prev = (
        cell.north, cell.east, cell.south, cell.west,
        neighbor.north, neighbor.east, neighbor.south, neighbor.west
        )

        if direction == "N":
            cell.north = False
            neighbor.south = False
        elif direction == "E":
            cell.east = False
            neighbor.west = False
        elif direction == "S":
            cell.south = False
            neighbor.north = False
        elif direction == "W":
            cell.west = False
            neighbor.east = False
        
        # check fo 3x3 open areas
        if self._creates_3x3_open(x, y):
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

                if not (0 <= cx <= self.width - 3 and 0 <= cy <= self.height - 3):
                    continue

                if self._is_3x3_open(cx, cy):
                    return True
        return False
    
    def _is_3x3_open(self, x: int, y: int) -> bool:
        """Return True if the 3x3 block at (x,y) is fully open inside."""

        for j in range(3):
            for i in range(3):
                cell = self.grid[y + j][x + i]

                if i < 2:
                    if cell.east:
                        return False

                if j < 2:
                    if cell.south:
                        return False
        return True


    def solve(
        self,
        entry: Tuple[int, int],
        exit: Tuple[int, int]
    ) -> str:
        """Return shortest path as NESW string."""
        queue = deque([(entry, "")])
        visited = set([entry])

        while queue:
            # time.sleep(0.25)
            (x, y), path = queue.popleft()
            if (x, y) == exit:
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
                # Convert value to hex and add it to the hex_row string
                hex_row += format(value, "X")
            rows.append(hex_row)
        return rows
    def export(self, file_path, entry, exit_, solution):
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

    def _apply_42(self):
        closed_cells = self.forty_two.get_cells()
        for (x, y) in closed_cells:

            cell = self.grid[y][x]

            cell.north = True
            cell.south = True
            cell.east = True
            cell.west = True
