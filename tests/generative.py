from array import array
from itertools import islice, tee
from typing import Dict, Tuple, Any
from urllib.request import urlopen

import json

from wordsearch.grid import Vector, Grid, vector
from wordsearch.puzzle import find_word

directions = [
  (0, -1),
  (1, -1),
  (1, 0),
  (1, 1),
  (0, 1),
  (-1, 1),
  (-1, 0),
  (-1, -1)
]

def parse_answer(answer: Dict[str, Any]) -> Tuple[str, Vector]:
  word = answer['w'].replace(' ', '')
  column = answer['c']
  row = answer['r']
  direction = answer['d']
  horizonal, vertical = directions[direction]

  return word, islice(vector(horizonal, vertical, (column, row)), len(word))

games = urlopen('https://staging.puzzlexperts.com/YouPlay/api/game/6/archive').read()

for metadata in json.loads(games):
  puzzle_id = metadata['puzzleId']
  response = urlopen(f"https://staging.puzzlexperts.com/YouPlay/api/game/data2/6/{puzzle_id}").read()

  game = json.loads(response)
  grid = Grid(array('I', map(ord, game['g'])))
  answers = map(parse_answer, game['w'])

  for (word, answer) in answers:
    output, result = tee(find_word(grid, word))
    print(f"{word}:", ', '.join(map(str, output)))

    assert(list(result) == list(answer))
