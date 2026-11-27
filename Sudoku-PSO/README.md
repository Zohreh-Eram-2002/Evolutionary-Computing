# Sudoku Solver — Particle Swarm Optimization (PSO)

Solves a standard 9×9 Sudoku puzzle using **PSO** and shows an **animation** of the solution being filled in, step by step.

## How it works

| Concept | Implementation |
|---|---|
| **Particle** | A complete 9×9 grid where each row is a permutation of 1–9 (clue cells fixed) |
| **Fitness** | Count of distinct values across all rows, columns, and 3×3 boxes (max = 243) |
| **Cognitive move** | Mutate a particle toward its personal best (swap two free cells in a random row) |
| **Social move** | Mutate a particle toward the global best |
| **Stagnation restart** | Re-randomise the worst half of the swarm when no improvement for N iterations |

## Run in Google Colab

```python
# 1 — clone or upload sudoku_pso.py, then:
!pip install matplotlib numpy   # already installed in Colab

%run sudoku_pso.py
```

Or paste the whole file into a Colab cell and run it.

## Parameters (inside the script)

```python
pso_solve(puzzle,
          n_particles    = 200,   # swarm size
          max_iter       = 2000,  # maximum iterations
          stagnation_limit = 100) # iterations without improvement → restart
```

Increase `n_particles` or `max_iter` for harder puzzles.

## Change the puzzle

Edit the `PUZZLE` array at the top of `sudoku_pso.py`. Use `0` for empty cells:

```python
PUZZLE = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    ...
])
```

## Output

- **Console** — iteration number and score when the puzzle is solved  
- **Animation** — the grid being filled in; clues shown in **dark navy**, PSO-filled cells in **red**

## Requirements

```
numpy
matplotlib
```
