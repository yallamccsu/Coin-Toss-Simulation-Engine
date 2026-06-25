# Coin Toss Simulation Engine

A Python-based probabilistic simulation engine for coin toss sequences. 
Runs a configurable number of tosses, tracks outcome frequency, and 
generates a structured post-session report including streak analysis.

## Features

- Simulates any number of coin tosses via a configurable constant
- Tracks heads and tails frequency with percentage breakdown
- Identifies the longest consecutive streak and the face it belongs to
- Full toss log maintained across the session
- Input validation handles NaN, infinite values, and zero counts
- Optional RNG seeding for reproducible simulation runs

## How to Run

```bash
python CoinToss.py
```

No external dependencies. Requires Python 3 with a standard installation.

## Sample Output

```
coin toss simulator

  toss 1: heads
  toss 2: tails
  toss 3: heads
  ...

  summary
  --------------------
  heads: 6 (60.0%)
  tails: 4 (40.0%)
  longest streak: 3x heads
```

## Technical Highlights

- `Face` enum replaces magic integers for clean outcome representation
- Weighted distribution pipeline built via `functools.reduce` even for a fair coin
- `TossResult` dataclass captures full state of every individual toss
- `SimulationReport` auto-computes frequency, percentages, and streak on initialization
- `CoinEngine` maintains an isolated RNG and full session log
- Rendering logic fully separated from simulation logic

## Tech Stack

Python 3 | dataclasses | enums | functools | collections
