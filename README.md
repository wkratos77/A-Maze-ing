*This project has been created as part of the 42 curriculum by wkrati, hjalzim.*

# A-Maze-ing

## Description

A-Maze-ing is a Python project whose goal is to **generate and visualize mazes in the terminal**.

The project is divided into two main components:

1. A **maze generation module** implemented as a reusable Python package called `mazegen`.
2. A **visualization interface** that displays the generated maze in the terminal using the `curses` library.

The program reads a configuration file that defines the maze parameters such as size, entry and exit points, and generation options.  
Using these parameters, a maze is generated and then displayed interactively.

The generated maze follows several constraints:

- The maze is surrounded by walls.
- All cells are reachable.
- There is no open 3×3 area in the maze.
- A **“42” pattern** is embedded inside the maze when the maze size allows it.
- If the *perfect* option is enabled, there is only **one unique path between any two points**.
- When a seed is provided, the same maze can be reproduced.

---

# Instructions

## Requirements

- Python 3.10+
- Terminal supporting `curses`
- `flake8`
- `mypy`

Install dependencies if needed:

```bash
pip install flake8 mypy build
```
---

## Running the program

The program takes a configuration file as argument.
```bash
python3 a_maze_ing.py config.txt
```
This will:

1. Parse the configuration file

2. Generate a maze

3. Display it interactively in the terminal

---

## Controls

During visualization:

|Key	  | Action
|------:|------------------|
R	      |regenerate a new maze
Q	      |quit the program
P       |solve path
H       |hide path
C       |change color
T       |change 42 color

---

## Linting
```
make lint
```
Runs:

- flake8

- mypy

## Building the reusable package
```
make build
```
This creates the package inside dist/.

You can install it with:
```
pip install dist/mazegen-*.tar.gz
```
---

## Configuration File

The configuration file contains the parameters used to generate the maze.

Example:
```
WIDTH=31
HEIGHT=21
ENTRY=1,0
EXIT=29,20
PERFECT=True
SEED=42
```
---

## Parameters
Parameter|	Description
|------:|------------------|
WIDTH|	Maze width
HEIGHT|	Maze height
ENTRY|	Entry coordinates
EXIT	|Exit coordinates
PERFECT|	Enable perfect maze generation
SEED|	Random seed used for deterministic generation

Using the same seed will always generate the same maze.

---

## Maze Generation Algorithm

The maze generation is implemented in the mazegen package.

The algorithm used is Recursive Backtracking (Depth-First Search maze generation).

### Algorithm overview

1. Start from an initial cell.

2. Mark it as visited.

3. Randomly choose an unvisited neighbor.

4. Remove the wall between the current cell and the chosen neighbor.

5. Move to the neighbor and repeat.

6. If a cell has no unvisited neighbors, backtrack to the previous cell.

This continues until every cell has been visited.

---

## Why This Algorithm

Recursive Backtracking was chosen because:

- It is simple and reliable.

- It guarantees a perfect maze (a single path between any two cells).

- It produces visually interesting maze structures.

- It is efficient and easy to implement.

This algorithm is widely used in maze generation problems and fits the project constraints well.

---

## Reusable Code

The reusable part of this project is the mazegen package.

This module contains:
```
mazegen/
    generator.py
    show_the_exit.py
```
It can be used independently in other projects.

Example usage:
```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=31, height=21, seed=42)
maze = generator.generate()
```
The visualization system is separate from the generator, allowing the generation logic to be reused in different environments.

---

# Team and Project Management
## Roles

The project was divided into two main parts.

### Visualisation, parsing and program interface

#### Walid Krati (wkrati)

Responsible for:

- Project architecture and integration
- Terminal visualization using `curses`
- Interactive interface
- Maze rendering
- Configuration file parsing
- Main program entry point
- Build system and project tooling
  - Makefile
  - pyproject.toml
  - requirements management
  - package building
- Packaging and reusable module integration
- Linting configuration (`flake8`, `mypy`)
- Project documentation

Implemented files:
```
visualisation/display.py
visualisation/parsing.py
a_maze_ing.py
Makefile
pyproject.toml
requirements.txt
```
### Maze Generation Module

#### Hamza Jalzim (hjalzim)

Responsible for:

- Maze generation algorithm
- Pathfinding validation between entry and exit
- Integration of maze constraints

Implemented files:
```
mazegen/generator.py
mazegen/show_the_exit.py
```
---

## Planning and Evolution
### Initial Planning

The project was divided early into two independent parts:

1. Maze generation module

2. Visualization and program interface

This allowed both contributors to work in parallel.

### How it evolved

During development:

- The maze generation module was implemented first.
- The visualization system was developed and connected to the generator.
- Additional work was done to ensure that the generator could function as a reusable package.
- Packaging and project tooling were added to allow rebuilding and installing the `mazegen` module.
- Additional validation was added to ensure maze correctness.

- Clear separation between the generation module and the visualization system.
- Modular design allowing the generator to be reused independently.
- Strong integration between configuration parsing, generation, and visualization.

### What Could Be Improved

- Earlier integration testing between modules.
- More automated validation tests for edge cases.

---

## Tools Used

- Python
- curses
- flake8
- mypy
- build
- Git

---

## Resources

Maze generation:

- https://en.wikipedia.org/wiki/Maze_generation_algorithm

- https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking

- https://www.redblobgames.com/pathfinding/

Python documentation:

- https://docs.python.org/3/

- https://docs.python.org/3/library/curses.html

---

## AI Usage

AI tools were used only as assistance during development for:

- Debugging explanations

- Understanding Python packaging

- Clarifying maze generation concepts

- AI was not used to generate the core algorithms or replace the development work.

All implementation decisions, structure, and final code were written and validated by the project contributors.
