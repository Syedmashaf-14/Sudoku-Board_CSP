# Sudoku CSP Solver
A Python-based Sudoku solver built using Constraint Satisfaction Problem (CSP) techniques. It combines AC-3 arc consistency, forward checking, and backtracking with the Minimum Remaining Values (MRV) heuristic to efficiently solve Sudoku puzzles of varying difficulty.
## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Input Format](#input-format)
- [Usage](#usage)
- [Output](#output)
- [Performance Metrics](#performance-metrics)
- [Algorithm Details](#algorithm-details)

## Overview

This solver treats Sudoku as a classic CSP where each cell is a variable, the digits 1 through 9 form the domain, and the constraint is that no two cells in the same row, column, or 3x3 box may share the same value. Three AI techniques are layered together to minimize the search space before and during backtracking.

---

## How It Works

The solver applies three strategies in combination:

1. AC-3 (Arc Consistency 3) runs first to prune domains globally before any search begins.
2. Forward Checking eliminates values from neighboring cells each time an assignment is made.
3. Backtracking Search explores possible assignments, guided by the MRV heuristic which always picks the variable with the fewest remaining legal values.

This layered approach dramatically reduces the number of backtracks needed, especially for harder puzzles.

---

## Project Structure

```
sudoku-csp-solver/
    sudoku_csp.py       Main solver implementation
    easy.txt            Easy difficulty puzzle
    medium.txt          Medium difficulty puzzle
    hard.txt            Hard difficulty puzzle
    veryhard.txt        Very hard difficulty puzzle
    README.md           Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- No external libraries required

### Installation

Clone the repository and navigate into the project folder:

```bash
git clone https://github.com/your-username/sudoku-csp-solver.git
cd sudoku-csp-solver
```

---

## Input Format

Each puzzle must be a plain text file containing exactly 9 lines, with each line holding exactly 9 digits. Use 0 to represent an empty cell.

Example (easy.txt):

```
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
```

The solver validates the format on load and raises a descriptive error if the file does not match the expected structure.

---

## Usage

Place your puzzle files in the same directory as sudoku_csp.py, then run:

```bash
python sudoku_csp.py
```

By default the script attempts to solve four files: easy.txt, medium.txt, hard.txt, and veryhard.txt. Files that are not found are skipped with a notification. To solve a different set of puzzles, edit the files list near the bottom of sudoku_csp.py:

```python
files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
```

---

## Output

For each puzzle the solver prints the completed grid followed by performance metrics:

```
Attempting to solve easy.txt...
--- Solution for easy.txt ---
5 3 4 6 7 8 9 1 2
6 7 2 1 9 5 3 4 8
1 9 8 3 4 2 5 6 7
8 5 9 7 6 1 4 2 3
4 2 6 8 5 3 7 9 1
7 1 3 9 2 4 8 5 6
9 6 1 5 3 7 2 8 4
2 8 7 4 1 9 6 3 5
3 4 5 2 8 6 1 7 9
------------------------------
Metrics for easy.txt:
 - BACKTRACK Calls: 1
 - BACKTRACK Failures: 0
 - Time taken: 0.0021 seconds
```

If no solution exists, the solver prints a clear message and exits gracefully.

---

## Performance Metrics

The solver tracks and reports three metrics for every puzzle:

| Metric | Description |
|---|---|
| BACKTRACK Calls | Total number of times the backtracking function was invoked |
| BACKTRACK Failures | Number of times a branch was abandoned due to no valid value |
| Time Taken | Wall-clock time in seconds from start to solution |

Lower backtrack calls and failures indicate that AC-3 and forward checking successfully pruned the search space before guessing was needed.

---

## Algorithm Details

### Variables and Domains

Every cell (row, column) is a variable. Pre-filled cells have a singleton domain containing their given digit. Empty cells start with a domain of {1, 2, 3, 4, 5, 6, 7, 8, 9}.

### Constraints and Neighbors

Two cells are neighbors if they share a row, a column, or a 3x3 box. The constraint between any pair of neighbors is simply that they must hold different values.

### AC-3

AC-3 processes a queue of arcs (Xi, Xj). For each arc it removes any value from Xi's domain that has no consistent value in Xj's domain. When a domain shrinks, all arcs pointing to Xi are re-added to the queue. If any domain reaches zero, the puzzle is determined to be unsolvable at that point.

### Forward Checking

After assigning a value to a variable, forward checking immediately removes that value from the domains of all unassigned neighbors. If any neighbor's domain becomes empty, the assignment is undone and the next value is tried.

### MRV Heuristic

The Minimum Remaining Values heuristic selects the unassigned variable whose domain is smallest. This fail-first strategy surfaces conflicts early, reducing unnecessary exploration of dead-end branches.

### Backtracking

When neither AC-3 nor forward checking can fully determine the solution, backtracking takes over. It assigns values one variable at a time, using deep copies of the domain state so that failed branches can be rolled back cleanly.

---
