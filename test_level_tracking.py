#!/usr/bin/env python3
"""
Demonstrate level-based transition tracking.
"""

from probability_transition_simulator import simulate_transitions, print_summary


def main():
    # Define transition probabilities
    # Format: [P_success, P_break, P_fail, P_downgrade]
    transition_array = [
        [0.6, 0.1, 0.2, 0.1],   # Level 0
        [0.5, 0.15, 0.2, 0.15], # Level 1
        [0.4, 0.2, 0.2, 0.2],   # Level 2
    ]

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=0,
        target_level=3,
        num_simulations=1000,
        random_seed=42
    )

    # Print full summary with level breakdown
    print_summary(stats, num_simulations=1000)

    # Access specific level statistics programmatically
    print("\n" + "=" * 50)
    print("PROGRAMMATIC ACCESS TO LEVEL STATS")
    print("=" * 50)

    for level in range(3):
        level_stats = stats.get_level_stats(level)
        print(f"\nLevel {level}: {level_stats}")

    # Compare break vs fail at different levels
    print("\n" + "=" * 50)
    print("BREAK vs FAIL COMPARISON")
    print("=" * 50)

    for level in range(3):
        breaks = stats.break_by_level.get(level, 0)
        fails = stats.fail_by_level.get(level, 0)
        total_same_level = breaks + fails

        if total_same_level > 0:
            print(f"\nLevel {level}:")
            print(f"  Breaks: {breaks} ({100 * breaks / total_same_level:.1f}% of same-level transitions)")
            print(f"  Fails:  {fails} ({100 * fails / total_same_level:.1f}% of same-level transitions)")

    # Find which level had the most downgrades
    print("\n" + "=" * 50)
    print("LEVEL WITH MOST DOWNGRADES")
    print("=" * 50)

    if stats.downgrade_by_level:
        max_downgrade_level = max(stats.downgrade_by_level, key=stats.downgrade_by_level.get)
        max_downgrades = stats.downgrade_by_level[max_downgrade_level]
        print(f"Level {max_downgrade_level} had the most downgrades: {max_downgrades}")


if __name__ == "__main__":
    main()
