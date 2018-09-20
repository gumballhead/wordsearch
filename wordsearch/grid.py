from array import array
from math import sqrt
from itertools import takewhile, product
from collections.abc import Mapping
from typing import Iterator, Tuple

Coordinates = Tuple[int, int]
Direction = Tuple[int, int]
Vector = Iterator[Coordinates]

def vector(start: Coordinates, direction: Direction) -> Vector:
  """Generates points from a starting position in a constant direction"""
  x, y = start
  horizontal, vertical = direction

  while True:
    yield (x, y)
    x += horizontal
    y += vertical

def terminal(start: Coordinates, direction: Direction, distance: int) -> Coordinates:
  """Calculate the terminal position of a vector given a starting position and length"""
  x, y = start
  horizontal, vertical = direction
  length = distance - 1

  return (x + horizontal * length, y + vertical * length)

def directions() -> Iterator[Direction]:
  """Create an iterator over the product of all horizontal and vertical directions"""
  return filter(lambda it: it != (0, 0), product((-1, 0, 1), (-1, 0, 1)))

class Grid(Mapping):
  """
  An abstraction to represent a puzzle grid. Grid wraps a single dimension array of characters
  and maps between array addresses and grid coordinate pairs.

  This class allows indexing into the character array based on (column, row) coordinate pairs. This is
  convenient for traversing the grid in two dimensions to search for words. See the `vector` method.
  """

  characters: array

  def __init__(self, characters: array) -> None:
    length = len(characters)
    size = int(sqrt(length))

    if size ** 2 != length:
      raise ValueError('Character array length for a Grid must be a perfect square (rows = columns)')

    self.characters = characters

  def __getitem__(self, coordinates: Coordinates) -> str:
    """Allows indexing of the character array by grid coordinates"""
    if coordinates not in self:
      raise KeyError(f"Coordinate pair {coordinates} outside of grid extent")

    i = self.address(coordinates)
    return chr(self.characters[i])

  def __iter__(self) -> Iterator[Coordinates]:
    """Return an iterator over all points in the grid"""
    return map(self.coordinates, range(len(self)))

  def __len__(self) -> int:
    """Return the number of characters in the grid"""
    return len(self.characters)

  def __contains__(self, key: object) -> bool:
    """Returns a boolean indicating whether a coordinate pair lies within the grid extent"""
    if not isinstance(key, tuple):
      return False

    x, y = key

    if isinstance(x, int) and isinstance(y, int):
      size = self.size
      return (0 <= x < size) and (0 <= y < size)
    else:
      return False

  @property
  def size(self) -> int:
    """Compute the size (width = height) of the grid square"""
    return int(sqrt(len(self.characters)))

  def address(self, coordinates: Coordinates) -> int:
    """Calculate the array address for a given coordinate pair using row major order"""
    column, row = coordinates
    return self.size * row + column

  def coordinates(self, address: int) -> Coordinates:
    """Calculate the point coordinates of a given address using row major order"""
    size = self.size
    row = address // size
    column = address % size

    return (column, row)

  def vector(self, start: Coordinates, direction: Direction) -> Vector:
    """
    Generate a vector of coordinates from the grid based on a starting position and constant direction.
    The vector terminates at the grid extent and does not wrap.
    """
    return takewhile(self.__contains__, vector(start, direction))
