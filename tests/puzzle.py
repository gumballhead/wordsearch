import io
from unittest import TestCase

from wordsearch import puzzle

puzzle_input = io.StringIO('\n'.join([
  'BONES,KHAN,KIRK,SCOTTY,SPOCK,SULU,UHURA',
  'U,M,K,H,U,L,K,I,N,V,J,O,C,W,E',
  'L,L,S,H,K,Z,Z,W,Z,C,G,J,U,Y,G',
  'H,S,U,P,J,P,R,J,D,H,S,B,X,T,G',
  'B,R,J,S,O,E,Q,E,T,I,K,K,G,L,E',
  'A,Y,O,A,G,C,I,R,D,Q,H,R,T,C,D',
  'S,C,O,T,T,Y,K,Z,R,E,P,P,X,P,F',
  'B,L,Q,S,L,N,E,E,E,V,U,L,F,M,Z',
  'O,K,R,I,K,A,M,M,R,M,F,B,A,P,P',
  'N,U,I,I,Y,H,Q,M,E,M,Q,R,Y,F,S',
  'E,Y,Z,Y,G,K,Q,J,P,C,Q,W,Y,A,K',
  'S,J,F,Z,M,Q,I,B,D,B,E,M,K,W,D',
  'T,G,L,B,H,C,B,E,C,H,T,O,Y,I,K',
  'O,J,Y,E,U,L,N,C,C,L,Y,B,Z,U,H',
  'W,Z,M,I,S,U,K,U,R,B,I,D,U,X,S',
  'K,Y,L,B,Q,Q,P,M,D,F,C,K,E,A,B']))

class PuzzleTest(TestCase):
  puzzle = puzzle.read_puzzle(puzzle_input)

  def test_read_puzzle(self):
    words, grid = self.puzzle

    self.assertEqual(words, ['BONES', 'KHAN', 'KIRK', 'SCOTTY', 'SPOCK', 'SULU', 'UHURA'])
    self.assertEqual(len(grid), 225)
    self.assertEqual(grid.size, 15)
    self.assertEqual(grid[0, 0], 'U')
    self.assertEqual(grid[14, 14], 'B')

  def test_find_all(self):
    _, grid = self.puzzle
    *_, last = puzzle.find_all(grid, 'B')
    self.assertEqual(last, (14, 14))

  def test_directions(self):
    self.assertEqual(set(puzzle.directions()), {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)})

  def test_find_word(self):
    _, grid = self.puzzle

    self.assertEqual(list(puzzle.find_word(grid, 'BONES')), [(0, 6), (0, 7), (0, 8), (0, 9), (0, 10)])
    self.assertEqual(list(puzzle.find_word(grid, 'KHAN')), [(5, 9), (5, 8), (5, 7), (5, 6)])
    self.assertEqual(list(puzzle.find_word(grid, 'KIRK')), [(4, 7), (3, 7), (2, 7), (1, 7)])
    self.assertEqual(list(puzzle.find_word(grid, 'SCOTTY')), [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)])
    self.assertEqual(list(puzzle.find_word(grid, 'SPOCK')), [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)])
    self.assertEqual(list(puzzle.find_word(grid, 'SULU')), [(3, 3), (2, 2), (1, 1), (0, 0)])
    self.assertEqual(list(puzzle.find_word(grid, 'UHURA')), [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)])

    with self.assertRaises(ValueError):
      puzzle.find_word(grid, 'CHEKOV')

    # Should fail early if passed a word less than 2 characters long
    with self.assertRaises(ValueError):
      puzzle.find_word(grid, 'A')
