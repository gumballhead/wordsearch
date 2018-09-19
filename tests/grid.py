from unittest import TestCase
from array import array
from itertools import islice

from wordsearch.grid import Coordinates, Grid

class GridTest(TestCase):
  characters = 'UMKHU' + 'LKINV' + 'JOCWE' + 'LLSHK' + 'ZZWZC'
  grid = Grid(array('I', map(ord, characters)))

  def test_index(self):
    self.assertEqual(self.grid[(0, 0)], 'U')
    self.assertEqual(self.grid[(4, 0)], 'U')

    self.assertEqual(self.grid[(0, 1)], 'L')
    self.assertEqual(self.grid[(4, 1)], 'V')

    self.assertEqual(self.grid[(2, 2)], 'C')
    self.assertEqual(self.grid[(3, 3)], 'H')

    self.assertEqual(self.grid[(0, 4)], 'Z')
    self.assertEqual(self.grid[(4, 4)], 'C')

    with self.assertRaises(KeyError):
      self.grid[(5, 5)]

  def test_iterator(self):
    self.assertEqual(''.join(self.grid.values()), self.characters)

  def test_contains(self):
    self.assertTrue((0, 0) in self.grid)
    self.assertTrue((2, 2) in self.grid)
    self.assertTrue((4, 4) in self.grid)

    self.assertFalse((5, 4) in self.grid)
    self.assertFalse((5, 5) in self.grid)
    self.assertFalse((-1, -1) in self.grid)

    self.assertFalse('foo' in self.grid)
    self.assertFalse(None in self.grid)
    self.assertFalse(('foo', 'bar') in self.grid)

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
    self.assertEqual(self.grid.coordinates(0), (0, 0))
    self.assertEqual(self.grid.coordinates(6), (1, 1))
    self.assertEqual(self.grid.coordinates(12), (2, 2))
    self.assertEqual(self.grid.coordinates(18), (3, 3))
    self.assertEqual(self.grid.coordinates(24), (4, 4))

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
