from array import array
from itertools import chain
from typing import Tuple, List, TextIO

from wordsearch.grid import Grid

def parse_line(line: str) -> List[str]:
  return line.rstrip('\n').split(',')

def read_puzzle(lines: TextIO) -> Tuple[List[str], Grid]:
  words = parse_line(lines.readline())
  characters = map(ord, chain(*map(parse_line, lines)))
  return words, Grid(array('I', characters))
