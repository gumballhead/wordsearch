from array import array
from itertools import chain, product, islice, tee
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
  """Finds a word by searching in all direction of a grid, returning the location of each letter"""
  first_letter = word[0]
  length = len(word)

  if length < 2:
    raise ValueError(f"Search word must be at least two characters long! Got '{word}'")

  for x, y in find_all(grid, first_letter):
    # Generate search vectors in all possible directions starting from the first letter
    search_vectors = (grid.vector((x, y), horizontal, vertical) for horizontal, vertical in directions()

      # Filter out search vectors that terminate before the word ends (borders approaching an edge)
      if (x + horizontal * (length - 1), y + vertical * (length - 1)) in grid)

    for search_vector in search_vectors:
      # Limit the search vector to the length of the word and save a reference to return if it matches the word
      points, result = tee(islice(search_vector, length))

      # Translate the point vector to the character at each coordinate location
      characters = map(lambda it: grid[it], points)

      # Compare each character of the word to the characters in the search vector, returning early if no match found
      if all(a == b for a, b in zip(word, characters)):
        return result

  raise ValueError(f"{word} not found in puzzle!")
