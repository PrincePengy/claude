#!/usr/bin/env python3
"""
Probabilistic Transition Simulator

Simulates transitions between levels based on given probability distributions.
Each level has four possible outcomes: success (level up), break (stay),
fail (stay), or downgrade (level down).
"""

import random
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class TransitionStats:
    """Stores statistics about transitions during simulations."""
    success_count: int = 0
    break_count: int = 0
    fail_count: int = 0
    downgrade_count: int = 0
    total_steps: int = 0

    def add_transition(self, transition_type: str):
        """Record a transition."""
        if transition_type == 'success':
            self.success_count += 1
        elif transition_type == 'break':
            self.break_count += 1
        elif transition_type == 'fail':
            self.fail_count += 1
        elif transition_type == 'downgrade':
            self.downgrade_count += 1
        self.total_steps += 1

    def __str__(self):
        return (f"Total Steps: {self.total_steps}\n"
                f"  Success: {self.success_count}\n"
                f"  Break: {self.break_count}\n"
                f"  Fail: {self.fail_count}\n"
                f"  Downgrade: {self.downgrade_count}")


def simulate_transitions(
    transition_array: List[List[float]],
    start_level: int,
    target_level: int,
    num_simulations: int,
    verbose: bool = False,
    random_seed: int = None
) -> Tuple[TransitionStats, List[List[Tuple[int, int, str]]]]:
    """
    Simulate probabilistic transitions between levels.

    Parameters:
    -----------
    transition_array : List[List[float]]
        Array where transition_array[n] = [P_success, P_break, P_fail, P_downgrade]
        for level n. Probabilities should sum to 1.0 for each level.
    start_level : int
        Starting level for each simulation (N)
    target_level : int
        Target level to reach (M)
    num_simulations : int
        Number of simulations to run (K)
    verbose : bool
        If True, print detailed information about each simulation
    random_seed : int
        Random seed for reproducibility

    Returns:
    --------
    Tuple[TransitionStats, List[List[Tuple[int, int, str]]]]
        - Overall statistics across all simulations
        - List of simulation histories, where each history is a list of
          (from_level, to_level, transition_type) tuples
    """
    if random_seed is not None:
        random.seed(random_seed)

    overall_stats = TransitionStats()
    all_histories = []

    for sim_num in range(num_simulations):
        current_level = start_level
        simulation_history = []
        steps = 0

        if verbose:
            print(f"\n--- Simulation {sim_num + 1} ---")
            print(f"Starting at level {current_level}, target: {target_level}")

        while current_level != target_level:
            # Get probabilities for current level
            if current_level >= len(transition_array):
                raise ValueError(
                    f"Current level {current_level} exceeds transition array bounds "
                    f"(max level: {len(transition_array) - 1})"
                )

            probs = transition_array[current_level]
            p_success, p_break, p_fail, p_downgrade = probs

            # Validate probabilities sum to ~1.0
            prob_sum = sum(probs)
            if abs(prob_sum - 1.0) > 1e-6:
                raise ValueError(
                    f"Probabilities at level {current_level} sum to {prob_sum}, "
                    f"should sum to 1.0"
                )

            # Choose transition based on probabilities
            rand_val = random.random()
            cumulative = 0.0
            transitions = ['success', 'break', 'fail', 'downgrade']
            probabilities = [p_success, p_break, p_fail, p_downgrade]

            transition = None
            for trans, prob in zip(transitions, probabilities):
                cumulative += prob
                if rand_val < cumulative:
                    transition = trans
                    break

            # Fallback in case of floating point errors
            if transition is None:
                transition = transitions[-1]

            # Calculate next level
            old_level = current_level
            if transition == 'success':
                current_level += 1
            elif transition == 'downgrade':
                current_level -= 1
            # break and fail keep current_level the same

            # Ensure we don't go below level 0
            if current_level < 0:
                current_level = 0

            # Record transition
            simulation_history.append((old_level, current_level, transition))
            overall_stats.add_transition(transition)
            steps += 1

            if verbose:
                print(f"  Step {steps}: Level {old_level} -> {current_level} ({transition})")

            # Safety check to prevent infinite loops
            if steps > 100000:
                raise RuntimeError(
                    f"Simulation exceeded 100,000 steps. "
                    f"Check if target level {target_level} is reachable."
                )

        all_histories.append(simulation_history)

        if verbose:
            print(f"Reached target level {target_level} in {steps} steps")

    return overall_stats, all_histories


def print_summary(stats: TransitionStats, num_simulations: int):
    """Print summary statistics."""
    print("\n" + "=" * 50)
    print("SIMULATION SUMMARY")
    print("=" * 50)
    print(f"Number of simulations: {num_simulations}")
    print(f"\n{stats}")
    print(f"\nAverage steps per simulation: {stats.total_steps / num_simulations:.2f}")

    if stats.total_steps > 0:
        print("\nTransition Percentages:")
        print(f"  Success: {100 * stats.success_count / stats.total_steps:.2f}%")
        print(f"  Break: {100 * stats.break_count / stats.total_steps:.2f}%")
        print(f"  Fail: {100 * stats.fail_count / stats.total_steps:.2f}%")
        print(f"  Downgrade: {100 * stats.downgrade_count / stats.total_steps:.2f}%")


def example_usage():
    """Demonstrate the simulator with an example."""
    # Define transition probabilities for levels 0-5
    # Format: [P_success, P_break, P_fail, P_downgrade]
    transition_array = [
        [0.6, 0.1, 0.2, 0.1],  # Level 0
        [0.5, 0.15, 0.2, 0.15], # Level 1
        [0.4, 0.2, 0.2, 0.2],   # Level 2
        [0.35, 0.25, 0.2, 0.2], # Level 3
        [0.3, 0.3, 0.2, 0.2],   # Level 4
        [0.25, 0.35, 0.2, 0.2], # Level 5
    ]

    start_level = 0
    target_level = 3
    num_simulations = 1000

    print(f"Running {num_simulations} simulations from level {start_level} to level {target_level}")

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=start_level,
        target_level=target_level,
        num_simulations=num_simulations,
        verbose=False,  # Set to True to see individual simulation details
        random_seed=42
    )

    print_summary(stats, num_simulations)

    # Show a sample simulation
    print("\n" + "=" * 50)
    print("SAMPLE SIMULATION (first run)")
    print("=" * 50)
    for step_num, (from_lvl, to_lvl, trans_type) in enumerate(histories[0], 1):
        print(f"Step {step_num}: Level {from_lvl} -> {to_lvl} ({trans_type})")


if __name__ == "__main__":
    example_usage()
