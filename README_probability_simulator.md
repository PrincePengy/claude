# Probability Transition Simulator

A Python script for simulating probabilistic transitions between levels with four possible outcomes at each level.

## Overview

This simulator models a system where an entity progresses through levels (0, 1, 2, ..., N) with probabilistic transitions. At each level, there are four possible outcomes:

- **Success**: Transition to the next level (N → N+1)
- **Break**: Stay at the current level (N → N) - distinct event type
- **Fail**: Stay at the current level (N → N) - different from break
- **Downgrade**: Move down one level (N → N-1)

The key feature is that **break** and **fail** are tracked separately even though they result in the same state, which is useful for modeling systems where the *reason* for staying at the same level matters (e.g., equipment breaking vs. simply failing an upgrade).

## Files

- `probability_transition_simulator.py` - Main simulator module
- `example_usage.py` - Multiple examples showing different use cases
- `README_probability_simulator.md` - This file

## Quick Start

### Basic Usage

```python
from probability_transition_simulator import simulate_transitions, print_summary

# Define transition probabilities for each level
# Format: [P_success, P_break, P_fail, P_downgrade]
transition_array = [
    [0.6, 0.1, 0.2, 0.1],  # Level 0
    [0.5, 0.15, 0.2, 0.15], # Level 1
    [0.4, 0.2, 0.2, 0.2],   # Level 2
]

# Run 1000 simulations from level 0 to level 2
stats, histories = simulate_transitions(
    transition_array=transition_array,
    start_level=0,
    target_level=2,
    num_simulations=1000,
    random_seed=42  # Optional: for reproducibility
)

# Print summary statistics
print_summary(stats, num_simulations=1000)
```

### Function Parameters

**`simulate_transitions()`** - Main simulation function

Parameters:
- `transition_array` (List[List[float]]): Probabilities for each level
  - Each element: `[P_success, P_break, P_fail, P_downgrade]`
  - Probabilities must sum to 1.0 for each level
- `start_level` (int): Starting level (N)
- `target_level` (int): Target level to reach (M)
- `num_simulations` (int): Number of simulations to run (K)
- `verbose` (bool, optional): Print detailed step-by-step info (default: False)
- `random_seed` (int, optional): Random seed for reproducibility (default: None)

Returns:
- `TransitionStats`: Overall statistics across all simulations
- `List[List[Tuple[int, int, str]]]`: Detailed history of each simulation
  - Each history is a list of `(from_level, to_level, transition_type)` tuples

## Examples

### Example 1: Simple Simulation

```python
# Equipment upgrade system with increasing difficulty
transition_array = [
    [0.95, 0.02, 0.03, 0.0],   # Level 0→1: Very easy
    [0.70, 0.10, 0.15, 0.05],  # Level 1→2: Medium
    [0.30, 0.25, 0.30, 0.15],  # Level 2→3: Very hard
]

stats, histories = simulate_transitions(
    transition_array,
    start_level=0,
    target_level=3,
    num_simulations=100
)
```

### Example 2: Verbose Mode (Single Simulation)

```python
# See detailed step-by-step progression
stats, histories = simulate_transitions(
    transition_array,
    start_level=0,
    target_level=2,
    num_simulations=1,
    verbose=True  # Prints each step
)
```

Output:
```
--- Simulation 1 ---
Starting at level 0, target: 2
  Step 1: Level 0 -> 1 (success)
  Step 2: Level 1 -> 1 (break)
  Step 3: Level 1 -> 2 (success)
Reached target level 2 in 3 steps
```

### Example 3: Analyzing Histories

```python
stats, histories = simulate_transitions(
    transition_array,
    start_level=0,
    target_level=3,
    num_simulations=1000
)

# Analyze first simulation
first_sim = histories[0]
print(f"First simulation took {len(first_sim)} steps")

for step_num, (from_lvl, to_lvl, trans_type) in enumerate(first_sim, 1):
    print(f"Step {step_num}: {from_lvl} -> {to_lvl} ({trans_type})")

# Find longest simulation
longest_sim = max(histories, key=len)
print(f"Longest simulation: {len(longest_sim)} steps")

# Count break vs fail events
total_breaks = sum(1 for hist in histories for _, _, trans in hist if trans == 'break')
total_fails = sum(1 for hist in histories for _, _, trans in hist if trans == 'fail')
print(f"Total breaks: {total_breaks}, Total fails: {total_fails}")
```

### Example 4: Multiple Test Runs

See `example_usage.py` for comprehensive examples including:
- Simple progression systems
- Equipment upgrade mechanics
- Break vs. fail analysis
- Statistical analysis of results

## Use Cases

This simulator can model:

1. **Game Mechanics**
   - Equipment upgrade systems (break = item destroyed, fail = upgrade failed)
   - Character leveling with XP loss
   - Crafting systems with material loss

2. **Real-World Systems**
   - Learning progression (break = forgot material, fail = didn't improve)
   - Skill acquisition with regression
   - Quality control with defect tracking

3. **Research**
   - Markov chain analysis
   - Stochastic process modeling
   - Monte Carlo simulations

## Output Format

### TransitionStats Object

```python
Total Steps: 5000
  Success: 2500
  Break: 1000
  Fail: 1000
  Downgrade: 500
```

### Summary Statistics

```
Number of simulations: 1000
Average steps per simulation: 5.00

Transition Percentages:
  Success: 50.00%
  Break: 20.00%
  Fail: 20.00%
  Downgrade: 10.00%
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Running Examples

```bash
# Run the main example
python probability_transition_simulator.py

# Run comprehensive examples
python example_usage.py
```

## Notes

- Probabilities for each level must sum to 1.0 (validated automatically)
- Simulations have a safety limit of 100,000 steps to prevent infinite loops
- If `target_level` is unreachable given the probabilities, the simulation will timeout
- Random seed can be set for reproducible results
- The script distinguishes between "break" and "fail" events even though both keep the level unchanged

## License

Free to use and modify.
