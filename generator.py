import random
from typing import List, Tuple, Optional, Dict


class Cell:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.walls: dict = {
            'N': True,
            'E': True,
            'S': True,
            'W': True
        }
        self.visited: bool = False

    def check_walls(self, direction: str) -> List[str]:
        """
        Check if there's a wall in the given direction.
        Returns a list of directions where walls exist.
        """
        return self.walls[direction]

    def remove_wall(self, direction: str):
        """
        Remove the wall in the given direction.
        """
        self.walls[direction] = False

    def add_wall(self, direction: str):
        """
        Add a wall in the given direction.
        """
        self.walls[direction] = True


class Maze:
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int]):
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.cells: List[List[Cell]] = [
            [Cell(x, y) for y in range(height)]
            for x in range(width)]
        self.solution: List[str] = []

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """
        Get the cell at the specified coordinates.
        Returns None if the coordinates are out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x][y]
        return None

    def get_neighbors(self, x: int, y: int) -> List[Tuple[str, Cell]]:
        """
        Get the neighboring cells of the given cell.
        Returns a list of tuples containing the direction and the neighboring cell.
        """
        directions = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }
        neighbors = []
        for direction, (dx, dy) in directions.items():
            neighbor = self.get_cell(x + dx, y + dy)
            if neighbor:
                neighbors.append((direction, neighbor))
        return neighbors
    
class MazeGenerator:
    def __init__(self, width: int, height: int, perfect: bool = True,
                 loop_factor: float = 0.1, seed: Optional[int] = None):
        self.width: int = width
        self.height: int = height
        self.perfect: bool = perfect
        self.loop_factor: float = loop_factor
        self.seed: Optional[int] = seed

    def generate(self) -> Maze:
        """Generates a maze using a depth-first search algorithm.
        Returns:
            Maze: The generated maze object.
        """
        