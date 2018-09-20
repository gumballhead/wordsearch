from array import array
from math import sqrt
from itertools import takewhile
from collections.abc import Mapping
from typing import Iterator, Tuple, cast

Coordinates = Tuple[int, int]
Vector = Iterator[Coordinates]

def vector(horizontal: int, vertical: int, start=(0, 0)) -> Vector:
  """Generates points from a starting position in a constant direction"""
  x, y = start

  while True:
    yield (x, y)
    x += horizontal
    y += vertical

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

    if size * size != length:
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

    if not (isinstance(x, int) and isinstance(y, int)):
      return False

    size = self.size

    return (0 <= x < size) and (0 <= y < size)

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

  def vector(self, start: Coordinates, horizontal: int, vertical: int) -> Vector:
    """
    Generate a vector of coordinates from the grid based on a starting position and constant direction.
    The vector terminates at the grid extent and does not wrap.
    """
    return takewhile(self.__contains__, vector(horizontal, vertical, start))
