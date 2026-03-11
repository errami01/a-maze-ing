# mazegen

Reusable Python maze generator.

## Installation

pip install mazegen-1.0.0-py3-none-any.whl

## Basic Usage

from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=20,entry=(0, 0), exit(19, 19), seed=42)

gen.generate()

maze = gen.get_grid()

solution = gen.solve()

print(solution)

## Parameters

width : maze width
height : maze height
entry: (x, y)
exit: (x, y)
seed : optional random seed
perfect : generate perfect maze

## Accessing Maze Structure

maze = gen.get_grid()

This returns a 2D grid of Cell objects.
