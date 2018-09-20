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

  for x, y in find_all(grid, first_letter):
    # Generate search vectors in all possible directions starting from the first letter, and limit to the word length
    search_vectors = (islice(grid.vector((x, y), h, v), length) for (h, v) in directions()

      # Filter out search vectors that terminate before the word ends (borders approaching an edge)
      if (x + h * (length - 1), y + v * (length -1))  in grid)

    for search_vector in search_vectors:
      # Save a reference the points iterator to return as a result if it matches the word
      points, result = tee(search_vector)

      # Translate the point vector to the character at each coordinate location
      characters = map(lambda it: grid[it], points)

      # Compare each character of the word to the characters in the search vector, returning early if no match found
      if all(a == b for a, b in zip_longest(word, characters)):
        return result

  raise ValueError(f"{word} not found in puzzle!")
