*This project has been created as part of the 42 curriculum by msturma, aberrami.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generation and solving program written in Python.  
The program generates a maze based on parameters defined in a configuration file and exports the result to an output file. It also guarantees that the maze contains a visible **“42” pattern**, drawn using fully closed cells.

The goal of this project is to design a modular and reusable maze generation system while respecting software engineering practices such as:

- modular architecture
- reusable packages
- static analysis (flake8, mypy)
- automation with Makefile
- configuration-driven execution

The maze generator itself is implemented as a reusable Python package called **`mazegen`**, which can be packaged and installed independently.

---

# Instructions

## Installation

Install dependencies:
```bash
make install
```
## Run the program 
using Makfile
```bash
make run
```
or manually:
```bash
python3 a_maze_ing.py config.txt
```
## Debug mode
Run with Python debugger:
```bash
make debug
```
## Linting
Static analysis:
```bash
make lint
```
Strict checking:
```bash
make lint-strict
```
## Clean temporary files
```bash
make clean
```

# Configuration File Format
The program accepts a configuration file containing KEY=VALUE pairs.
Each line contains a single parameter.
Lines starting with # are treated as comments and ignored.
Example:
```ini
# Maze size
WIDTH=20
HEIGHT=15

# Entry and exit points
ENTRY=0,0   # Entry coordinates (x,y)
EXIT=19,14  # Exit coordinates (x,y)

# Output file
OUTPUT_FILE=maze.txt    # Name of output file

# Maze properties
PERFECT=True    # Whether the maze is perfect
SEED=42         # Optional random seed
ALGORITHM=DFS   # Optional Maze generation algorithm
```
# Maze Generation Algorithm
The maze is generated using the Depth-First Search (DFS) Backtracking algorithm.

## Algorithm overview

1. Start from the initial cell.
2. Mark the current cell as visited.
3. Randomly choose an unvisited neighbor.
4. Remove the wall between the current cell and the neighbor.
5. Move to the neighbor and repeat.
6. If no unvisited neighbors remain, backtrack.
7. This process continues until all cells have been visited.

## Why This Algorithm
The DFS backtracking algorithm was chosen because:
* it is simple to implement
* it guarantees a perfect maze (no loops and exactly one path between two cells)
* it produces natural-looking mazes
* it is memory efficient
* it is widely used in procedural maze generation

# Reusable Code
The reusable component of this project is the mazegen package.
Location:
```bash
src/mazegen/
```
Main class:
```bash
MazeGenerator
```
Example usage:
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=10, height=10, seed=42)

gen.generate()

maze = gen.get_grid()

solution = gen.solve()
```
The package exposes:
* maze generation
* maze solving
* access to the internal maze structure

The package can be built and installed using:
```bash
python -m build
pip install mazegen-1.0.0-py3-none-any.whl
```
This allows the generator to be reused in other projects.

# Maze Representation
Maze Representation:
* north
* east
* south
* west
Walls can be removed to create paths between cells.
The maze structure is stored internally as a 2D grid of Cell objects.

# Special Requirement: 42 Pattern
The maze must contain a visible “42” drawn with fully closed cells.

This pattern is embedded after maze generation by forcing specific cells to remain fully closed.