from sys import stdin
from wordsearch import puzzle

if stdin.isatty():
  exit('wordsearch script expects to run with a puzzle from std input. Usage: bin/wordsearch < puzzle')

words, grid = puzzle.read_puzzle(stdin)

for word in words:
  print(f"{word}:", ', '.join(map(str, puzzle.find_word(grid, word))))
