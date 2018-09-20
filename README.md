Wordsearch Puzzle Solver
========================
## Setup
```bash
git clone git@github.com:gumballhead/wordsearch.git
```

I chose to only use the python standard library in this solution, so there are no dependencies other than python3 and either linux or OS X.

## Commands
```bash
# Solve a wordsearch puzzle, where puzzle is a file containing a formatted puzzle
bin/wordsearch < puzzle

# Run all unit tests
bin/test

# Run an end-to-end test with data returned from a wordsearch puzzle archive api
bin/generative_test
```

Note that these need to be run from the project root.
