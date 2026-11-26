"""
N-Queens Problem Solver using Genetic Algorithm
================================================
Solves the N-Queens problem and animates the evolution process.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from IPython.display import HTML


# ─────────────────────────────────────────────
# 1.  GENETIC ALGORITHM CORE
# ─────────────────────────────────────────────

def random_chromosome(n: int) -> list[int]:
    """A chromosome is a permutation of [0..n-1]: queen in column i is at row chromosome[i]."""
    return random.sample(range(n), n)


def fitness(chromosome: list[int]) -> int:
    """
    Count non-attacking pairs.
    Max fitness = n*(n-1)/2  (all pairs non-attacking → solution found).
    """
    n = len(chromosome)
    max_pairs = n * (n - 1) // 2
    attacking = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Same row is impossible (permutation).
            # Check diagonal clash.
            if abs(chromosome[i] - chromosome[j]) == abs(i - j):
                attacking += 1
    return max_pairs - attacking


def select_parent(population: list, fitnesses: list[int]) -> list[int]:
    """Tournament selection (k=3)."""
    k = 3
    contestants = random.sample(list(zip(fitnesses, population)), k)
    return max(contestants, key=lambda x: x[0])[1]


def ordered_crossover(p1: list[int], p2: list[int]) -> list[int]:
    """Order-1 crossover that preserves the permutation property."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b+1] = p1[a:b+1]
    pointer = 0
    for gene in p2:
        if gene not in child:
            while child[pointer] != -1:
                pointer += 1
            child[pointer] = gene
    return child


def mutate(chromosome: list[int], rate: float) -> list[int]:
    """Swap mutation."""
    chrom = chromosome[:]
    if random.random() < rate:
        i, j = random.sample(range(len(chrom)), 2)
        chrom[i], chrom[j] = chrom[j], chrom[i]
    return chrom


def genetic_algorithm(
    n: int = 8,
    pop_size: int = 100,
    max_generations: int = 1000,
    mutation_rate: float = 0.1,
    elitism: int = 5,
    seed: int | None = None,
) -> dict:
    """
    Run the GA and return a history dict for animation.

    Returns
    -------
    dict with keys:
        'solution'     : best chromosome found (None if unsolved)
        'generations'  : list of best chromosomes per generation (for animation)
        'fitnesses'    : list of best fitness values per generation
        'max_fitness'  : n*(n-1)//2
        'solved'       : bool
        'n'            : n
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    max_fitness = n * (n - 1) // 2
    population = [random_chromosome(n) for _ in range(pop_size)]

    best_per_gen: list[list[int]] = []
    fit_per_gen: list[int] = []

    solution = None

    for gen in range(max_generations):
        fits = [fitness(c) for c in population]
        best_idx = int(np.argmax(fits))
        best_fit = fits[best_idx]
        best_chrom = population[best_idx][:]

        best_per_gen.append(best_chrom)
        fit_per_gen.append(best_fit)

        if best_fit == max_fitness:
            solution = best_chrom
            break

        # Elitism: carry top individuals unchanged
        sorted_pop = [c for _, c in sorted(zip(fits, population), key=lambda x: -x[0])]
        new_pop = sorted_pop[:elitism]

        while len(new_pop) < pop_size:
            p1 = select_parent(population, fits)
            p2 = select_parent(population, fits)
            child = ordered_crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_pop.append(child)

        population = new_pop

    return {
        "solution": solution,
        "generations": best_per_gen,
        "fitnesses": fit_per_gen,
        "max_fitness": max_fitness,
        "solved": solution is not None,
        "n": n,
    }


# ─────────────────────────────────────────────
# 2.  ANIMATION
# ─────────────────────────────────────────────

LIGHT_SQ = "#F0D9B5"
DARK_SQ  = "#B58863"
QUEEN_COLOR = "#2C3E50"
ATTACK_COLOR = "#E74C3C"
SAFE_COLOR   = "#27AE60"


def _queen_marker():
    """Return a Path object shaped like a simple queen crown."""
    # Using matplotlib's unicode text trick instead of a path
    return "♛"


def draw_board(ax, chromosome: list[int], n: int, generation: int,
               fitness_val: int, max_fitness: int):
    """Draw the chessboard with queens on axes `ax`."""
    ax.clear()
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw squares
    for row in range(n):
        for col in range(n):
            color = LIGHT_SQ if (row + col) % 2 == 0 else DARK_SQ
            rect = mpatches.FancyBboxPatch(
                (col, row), 1, 1,
                boxstyle="square,pad=0",
                facecolor=color, edgecolor="none"
            )
            ax.add_patch(rect)

    # Identify attacking queens
    attacking_cols = set()
    for i in range(n):
        for j in range(i + 1, n):
            if abs(chromosome[i] - chromosome[j]) == abs(i - j):
                attacking_cols.add(i)
                attacking_cols.add(j)

    # Draw queens
    for col, row in enumerate(chromosome):
        color = ATTACK_COLOR if col in attacking_cols else SAFE_COLOR
        ax.text(
            col + 0.5, row + 0.5, "♛",
            ha="center", va="center",
            fontsize=max(10, 160 // n),
            color=color,
            fontweight="bold",
        )

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)

    pct = int(100 * fitness_val / max_fitness)
    status = "✓ SOLVED!" if fitness_val == max_fitness else f"Fitness: {fitness_val}/{max_fitness}  ({pct}%)"
    title_color = SAFE_COLOR if fitness_val == max_fitness else "#2C3E50"
    ax.set_title(
        f"Generation {generation}   |   {status}",
        fontsize=13, fontweight="bold", color=title_color, pad=10
    )


def animate_ga(
    result: dict,
    interval: int = 120,
    max_frames: int = 200,
    fitness_panel: bool = True,
) -> FuncAnimation:
    """
    Build a FuncAnimation from the GA result history.

    Parameters
    ----------
    result        : dict returned by `genetic_algorithm()`
    interval      : ms between frames
    max_frames    : cap on total frames (subsampled if needed)
    fitness_panel : show fitness-over-generations subplot

    Returns
    -------
    FuncAnimation object (call .to_jshtml() or HTML(...) in Jupyter)
    """
    generations = result["generations"]
    fitnesses   = result["fitnesses"]
    max_fitness = result["max_fitness"]
    n           = result["n"]
    total       = len(generations)

    # Subsample if needed
    if total > max_frames:
        idx = list(range(0, total - 1, total // max_frames)) + [total - 1]
    else:
        idx = list(range(total))

    if fitness_panel:
        fig, (ax_board, ax_fit) = plt.subplots(
            1, 2, figsize=(12, 6),
            gridspec_kw={"width_ratios": [1, 1]}
        )
    else:
        fig, ax_board = plt.subplots(1, 1, figsize=(6, 6))
        ax_fit = None

    fig.patch.set_facecolor("#FAFAFA")

    if ax_fit is not None:
        ax_fit.set_facecolor("#F7F7F7")
        ax_fit.set_xlabel("Generation", fontsize=11)
        ax_fit.set_ylabel("Best Fitness", fontsize=11)
        ax_fit.set_title("Fitness over Generations", fontsize=12, fontweight="bold")
        ax_fit.set_xlim(0, total)
        ax_fit.set_ylim(0, max_fitness + 0.5)
        ax_fit.axhline(max_fitness, color=SAFE_COLOR, lw=1.5, ls="--", label="Max fitness")
        ax_fit.legend(fontsize=9)
        (line_fit,) = ax_fit.plot([], [], color="#3498DB", lw=2)
        (dot_fit,)  = ax_fit.plot([], [], "o", color="#E74C3C", ms=7)

    def update(frame_idx):
        i = idx[frame_idx]
        chrom = generations[i]
        fit   = fitnesses[i]
        draw_board(ax_board, chrom, n, i + 1, fit, max_fitness)

        if ax_fit is not None:
            x_data = list(range(i + 1))
            y_data = fitnesses[:i + 1]
            line_fit.set_data(x_data, y_data)
            dot_fit.set_data([i], [fit])

        return [ax_board] + ([line_fit, dot_fit] if ax_fit else [])

    anim = FuncAnimation(
        fig, update,
        frames=len(idx),
        interval=interval,
        blit=False,
    )
    plt.tight_layout()
    return anim


# ─────────────────────────────────────────────
# 3.  QUICK-RUN HELPER
# ─────────────────────────────────────────────

def solve_and_animate(
    n: int = 8,
    pop_size: int = 150,
    max_generations: int = 2000,
    mutation_rate: float = 0.15,
    elitism: int = 5,
    seed: int | None = 42,
    interval: int = 100,
    max_frames: int = 200,
) -> HTML:
    """
    One-liner: run GA then return an HTML animation for Jupyter.

    Example
    -------
    >>> from nqueens_ga import solve_and_animate
    >>> anim = solve_and_animate(n=8)
    >>> anim          # displays in Jupyter
    """
    print(f"Running GA for {n}-Queens …")
    result = genetic_algorithm(
        n=n,
        pop_size=pop_size,
        max_generations=max_generations,
        mutation_rate=mutation_rate,
        elitism=elitism,
        seed=seed,
    )

    gens = len(result["generations"])
    if result["solved"]:
        print(f"✓ Solution found in generation {gens}!")
        print(f"  Chromosome: {result['solution']}")
    else:
        best_fit = max(result["fitnesses"])
        print(f"✗ No perfect solution found after {gens} generations.")
        print(f"  Best fitness: {best_fit}/{result['max_fitness']}")

    anim = animate_ga(result, interval=interval, max_frames=max_frames)
    return HTML(anim.to_jshtml())
