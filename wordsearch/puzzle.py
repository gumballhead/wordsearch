from array import array
from itertools import chain, product, islice, tee, zip_longest
from typing import Tuple, List, Iterator, TextIO

from wordsearch.grid import Coordinates, Grid

def parse_line(line: str) -> List[str]:
  """Strip a line of its newline ending character and tokenize on comma separators"""
  return line.rstrip('\n').split(',')

def read_puzzle(lines: TextIO) -> Tuple[List[str], Grid]:
  """Reads a puzzle input file into the list of words and the character grid"""
  words = parse_line(lines.readline())
  characters = map(ord, chain(*map(parse_line, lines)))

  return words, Grid(array('I', characters))

def find_all(grid: Grid, letter: str) -> Iterator[Coordinates]:
  """Find the locations of each instance of a character in the grid"""
  for point, char in grid.items():
    if char == letter:
      yield point

def directions() -> Iterator[Tuple[int, int]]:
  """Generate all possible search directions"""
  return filter(lambda it: it != (0, 0), product((-1, 0, 1), (-1, 0, 1)))

def find_word(grid: Grid, word: str) -> Iterator[Coordinates]:
  """Finds a word by searching any direction in a grid, returning the location of each letter"""
  first_letter = word[0]
  length = len(word)

  for position in find_all(grid, first_letter):
    search_vectors = (islice(grid.vector(position, *direction), length) for direction in directions())

    for search_vector in search_vectors:
      points, result = tee(search_vector)
      characters = map(lambda it: grid[it], points)

      if all(a == b for a, b in zip_longest(word, characters)):
        return result

  raise ValueError(f"{word} not found in puzzle!")
