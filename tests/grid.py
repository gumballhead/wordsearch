from unittest import TestCase
from array import array
from itertools import islice

from wordsearch.grid import Grid

class GridTest(TestCase):
  characters = 'ABCDE' + 'FGHIJ' + 'KLMNO' + 'PQRST' + 'UVWXY'
  grid = Grid(array('I', map(ord, characters)))

  def test_init(self):
    with self.assertRaises(ValueError):
      Grid(array('I', map(ord, 'ABCDE')))

  def test_index(self):
    self.assertEqual(self.grid[0, 0], 'A')
    self.assertEqual(self.grid[3, 2], 'N')
    self.assertEqual(self.grid[3, 0], 'D')
    self.assertEqual(self.grid[2, 3], 'R')
    self.assertEqual(self.grid[4, 0], 'E')
    self.assertEqual(self.grid[2, 4], 'W')

    with self.assertRaises(KeyError):
      self.grid[5, 5]

  def test_iterator(self):
    self.assertEqual(''.join(self.grid.values()), self.characters)

  def test_contains(self):
    # Passing cases. Coordinates in grid
    self.assertTrue((0, 0) in self.grid)
    self.assertTrue((2, 2) in self.grid)
    self.assertTrue((4, 4) in self.grid)

    # Failing cases. Coordinates outside grid
    self.assertFalse((5, 4) in self.grid)
    self.assertFalse((5, 5) in self.grid)
    self.assertFalse((-1, -1) in self.grid)

    # Failing cases. Non-coordinate objects not in grid
    self.assertFalse('wat' in self.grid)
    self.assertFalse(1 in self.grid)
    self.assertFalse(None in self.grid)
    self.assertFalse(('foo', 'bar') in self.grid)
    self.assertFalse((1, 'too') in self.grid)

  def test_len(self):
    self.assertEqual(len(self.grid), 25)

  def test_size(self):
    self.assertEqual(self.grid.size, 5)

  def test_address(self):
    self.assertEqual(self.grid.address((0, 0)), 0)
    self.assertEqual(self.grid.address((1, 1)), 6)
    self.assertEqual(self.grid.address((2, 2)), 12)
    self.assertEqual(self.grid.address((3, 3)), 18)
    self.assertEqual(self.grid.address((4, 4)), 24)

  def test_coordinates(self):
    self.assertEqual(self.grid.coordinates(4), (4, 0))
    self.assertEqual(self.grid.coordinates(8), (3, 1))
    self.assertEqual(self.grid.coordinates(12), (2, 2))
    self.assertEqual(self.grid.coordinates(16), (1, 3))
    self.assertEqual(self.grid.coordinates(20), (0, 4))

  def test_vector(self):
    # Diagonal down and right
    first, *_, last = self.grid.vector((0, 0), 1, 1)
    self.assertEqual(first, (0, 0))
    self.assertEqual(last, (4, 4))

    # Straight right
    first, *_, last = self.grid.vector((0, 2), 1, 0)
    self.assertEqual(first, (0, 2))
    self.assertEqual(last, (4, 2))

    # Diagonal up and left
    first, *_, last = self.grid.vector((4, 4), -1, -1)
    self.assertEqual(first, (4, 4))
    self.assertEqual(last, (0, 0))

    # Straight up
    first, *_, last = self.grid.vector((2, 4), 0, -1)
    self.assertEqual(first, (2, 4))
    self.assertEqual(last, (2, 0))
