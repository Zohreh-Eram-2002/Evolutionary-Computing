# N-Queens Genetic Algorithm — Project Documentation

This project implements a Genetic Algorithm (GA) to solve the classic N-Queens problem — placing N queens on an N×N chessboard so that no two queens attack each other. The algorithm evolves a population of candidate solutions across generations, guided by a fitness function, until a perfect board arrangement is discovered. An animated visualisation inside Jupyter Notebook shows the board evolving in real time, with a fitness graph alongside. The repository contains a self-contained notebook, a reusable Python module, and this documentation.

## Problem Statement

The N-Queens problem asks: how can N queens be placed on an N×N chessboard so that no two queens share a row, column, or diagonal? Two queens attack each other when they occupy the same row, the same column, or either diagonal. For N = 8 (the classic version) there are exactly 92 distinct solutions out of 4,426,165,368 possible placements — making brute-force search impractical. The problem grows exponentially harder with N, motivating heuristic methods such as genetic algorithms.

## Genetic Algorithm Design

The GA represents each candidate solution as a permutation chromosome of length N. The value at index col gives the row of the queen in that column. Using a permutation guarantees no two queens share a row or column, so the algorithm only needs to eliminate diagonal conflicts.

Fitness: the number of non-attacking queen pairs. The maximum is N·(N−1)/2; a perfect score means all queens are safe and a solution has been found.

Selection: tournament selection (k = 3). Three individuals are sampled at random and the fittest is chosen as a parent. This creates selection pressure while preserving diversity.

Crossover: Order-1 (OX) crossover. A random segment is copied from parent 1; remaining positions are filled in the order they appear in parent 2. This always produces a valid permutation.

Mutation: swap mutation. With probability mutation\_rate, two genes are randomly swapped, allowing the algorithm to escape local optima.

Elitism: the top elitism individuals are carried unchanged into each new generation, preventing regression of the best solutions found.

## Implementation

The project contains four files:

- nqueens\_ga.py — reusable Python module with all GA logic and animation helpers
- N\_Queens\_GA.ipynb — self-contained Jupyter Notebook; all code is defined inline, no external file needed
- requirements.txt — pip dependencies: matplotlib, numpy, ipython, jupyter
- README.md — project overview for the GitHub repository page

Key functions in nqueens\_ga.py:

- random\_chromosome(n) — generates a random permutation of length n
- fitness(chromosome) — counts non-attacking queen pairs
- ordered\_crossover(p1, p2) — OX crossover preserving permutation validity
- mutate(chromosome, rate) — swap mutation
- genetic\_algorithm(...) — full GA loop; returns a history dict for animation
- animate\_ga(result, ...) — builds a FuncAnimation from GA history
- solve\_and\_animate(n, ...) — one-liner: run GA then return HTML animation

## Usage Guide

Install dependencies:

```bash
pip install -r requirements.txt
```

Open the notebook:

```bash
jupyter notebook N_Queens_GA.ipynb
```

Run cells 1 and 2 to install packages and define all functions, then use the one-liner:

```python
solve_and_animate(n=8, seed=42)  # displays animation inline
```

For full control, use the two-step API:

```python
result = genetic_algorithm(n=12, pop_size=200, max_generations=3000,
                           mutation_rate=0.15, elitism=10, seed=7)
anim = animate_ga(result, interval=120, max_frames=200, fitness_panel=True)
HTML(anim.to_jshtml())
```

Recommended hyperparameters by board size:

| N | pop\_size | max\_generations | mutation\_rate |
| --- | --- | --- | --- |
| 8 | 100 | 1 000 | 0.10 |
| 12 | 200 | 2 000 | 0.15 |
| 16 | 400 | 5 000 | 0.20 |

To save the animation as a GIF, install pillow then call anim.save('nqueens.gif', writer='pillow', fps=10).

## Animation

The animation produced by animate\_ga shows two panels side by side:

- Left — chessboard: light and dark squares in standard chess colours. Each queen is drawn as ♛. Green queens are safe (no diagonal clash with any other queen); red queens are in conflict.
- Right — fitness graph: a blue line tracking the best fitness per generation, with a green dashed target line at the maximum (perfect) fitness.

When the solution is found, all queens turn green and the title shows ✓ SOLVED! The animation is subsampled to at most max\_frames frames so large runs remain smooth. The interval parameter sets the milliseconds between frames.

## Results

Typical convergence with seed = 42 and default settings:

| N | Generations to solve | Approx. time |
| --- | --- | --- |
| 8 | < 100 | < 1 s |
| 12 | 100 – 500 | 1 – 5 s |
| 16 | 500 – 2 000 | 5 – 30 s |

Results are stochastic; exact values depend on the random seed and hyperparameters. GAs work well here because the permutation encoding eliminates row and column conflicts entirely, letting the algorithm focus exclusively on diagonal conflicts. Population diversity, recombination via crossover, and mutation allow it to explore the fitness landscape and escape local optima efficiently.

## GitHub Repository Setup

Follow these steps to publish the project as a public GitHub repository.

```bash
cd nqueens-ga

# 1. Initialise git and stage files
git init
git add N_Queens_GA.ipynb nqueens_ga.py README.md requirements.txt

# 2. First commit
git commit -m "Initial commit: N-Queens solver with Genetic Algorithm + Jupyter animation"

# 3. Create remote repo and push (requires GitHub CLI)
gh repo create nqueens-genetic-algorithm --public --source=. --remote=origin --push
```

Without the GitHub CLI, create an empty repo on github.com first, then:

```bash
git remote add origin https://github.com/<your-username>/nqueens-genetic-algorithm.git
git branch -M main
git push -u origin main
```

After pushing, add a one-line description and the topics n-queens, genetic-algorithm, jupyter-notebook, and python to make the repo discoverable.

## References

1\. Russell, S. & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson. Covers N-Queens (Section 4.1) and genetic algorithms (Section 4.4).

2\. Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization, and Machine Learning. Addison-Wesley. Foundational textbook on selection, crossover, and mutation operators.

3\. Wikipedia — N-Queens problem: https://en.wikipedia.org/wiki/Eight\_queens\_puzzle

4\. Wikipedia — Genetic algorithm: https://en.wikipedia.org/wiki/Genetic\_algorithm

5\. matplotlib FuncAnimation API: https://matplotlib.org/stable/api/animation\_api.html
