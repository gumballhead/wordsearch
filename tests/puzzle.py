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
  def setUp(self):
    self.puzzle = puzzle.read_puzzle(puzzle_input)

  def test_read_puzzle(self):
    words, grid = self.puzzle

    self.assertEqual(words, ['BONES', 'KHAN', 'KIRK', 'SCOTTY', 'SPOCK', 'SULU', 'UHURA'])
    self.assertEqual(len(grid.characters), 225)
    self.assertEqual(grid.size, 15)
    self.assertEqual(grid[0, 0], 'U')
    self.assertEqual(grid[14, 14], 'B')
