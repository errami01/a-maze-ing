"""
Reusable Maze Generator Module
"""

# from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
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

    def generate(self) -> None:
        """Generate a new maze."""

        # RESET GRID EACH TIME generated IS CALLED
        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        visited = set()
        stack = [(0, 0)]

        while stack:
            x, y = stack[-1]
            visited.add((x, y))

            neighbors = self._get_unvisited_neighbors(x, y, visited)

            if not neighbors:
                stack.pop()
                continue

            nx, ny, direction = self._rng.choice(neighbors)

            self._remove_wall(x, y, nx, ny, direction)

            stack.append((nx, ny))


    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int,
        visited: set[Tuple[int, int]]
    ) -> List[Tuple[int, int, str]]:
        neighbors = []

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
                (nx, ny) not in visited
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
    ) -> None:
        cell = self.grid[y][x]
        neighbor = self.grid[ny][nx]

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

    def solve(
        self,
        entry: Tuple[int, int],
        exit: Tuple[int, int]
    ) -> str:
        """Return shortest path as NESW string."""
        queue = deque([(entry, "")])
        visited = set([entry])

        while queue:
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
                hex_row += format(value, "X")
            rows.append(hex_row)
        return rows

    def _add_extra_connections(self) -> None:
        """Add random wall removals for non-perfect maze."""
        for _ in range((self.width * self.height) // 10):
            x = self._rng.randrange(self.width)
            y = self._rng.randrange(self.height)
            direction = self._rng.choice(["N", "E", "S", "W"])

            dx, dy = {
                "N": (0, -1),
                "E": (1, 0),
                "S": (0, 1),
                "W": (-1, 0),
            }[direction]

            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                self._remove_wall(x, y, nx, ny, direction)
