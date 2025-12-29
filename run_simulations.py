#!/usr/bin/env python3
"""
Run 1000 simulations with specific transition probabilities.

Table format from user: [Success, Fail, Downgrade, Break]
Code format required: [P_success, P_break, P_fail, P_downgrade]
"""

from probability_transition_simulator import simulate_transitions, print_summary


def main():
    # Define transition probabilities for levels 0-11
    # Format: [P_success, P_break, P_fail, P_downgrade]
    # Converted from user's table: [Success, Fail, Downgrade, Break]

    transition_array = [
        # Level 0: 100% success, 0% fail, 0% downgrade, 0% break
        [1.0, 0.0, 0.0, 0.0],

        # Level 1: 50% success, 50% fail, 0% downgrade, 0% break
        [0.5, 0.0, 0.5, 0.0],

        # Level 2: 33% success, 67% fail, 0% downgrade, 0% break
        [0.33, 0.0, 0.67, 0.0],

        # Level 3: 25% success, 75% fail, 0% downgrade, 0% break
        [0.25, 0.0, 0.75, 0.0],

        # Level 4: 25% success, 45% fail, 20% downgrade, 10% break
        [0.25, 0.10, 0.45, 0.20],

        # Level 5: 25% success, 45% fail, 20% downgrade, 10% break
        [0.25, 0.10, 0.45, 0.20],

        # Level 6: 20% success, 40% fail, 25% downgrade, 15% break
        [0.20, 0.15, 0.40, 0.25],

        # Level 7: 20% success, 40% fail, 25% downgrade, 15% break
        [0.20, 0.15, 0.40, 0.25],

        # Level 8: 20% success, 40% fail, 25% downgrade, 15% break
        [0.20, 0.15, 0.40, 0.25],

        # Level 9: 20% success, 40% fail, 25% downgrade, 15% break
        [0.20, 0.15, 0.40, 0.25],

        # Level 10: 20% success, 30% fail, 30% downgrade, 20% break
        [0.20, 0.20, 0.30, 0.30],

        # Level 11: 20% success, 30% fail, 30% downgrade, 20% break
        [0.20, 0.20, 0.30, 0.30],
    ]

    # Verify all probabilities sum to 1.0
    print("Verifying transition probabilities:")
    for level, probs in enumerate(transition_array):
        total = sum(probs)
        print(f"Level {level:2d}: {probs} = {total:.2f}")

    # Run simulations from level 0 to level 11
    start_level = 0
    target_level = 11
    num_simulations = 1000

    print(f"\n{'='*60}")
    print(f"Running {num_simulations} simulations")
    print(f"Start level: {start_level}")
    print(f"Target level: {target_level}")
    print(f"{'='*60}")

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=start_level,
        target_level=target_level,
        num_simulations=num_simulations,
        verbose=False,
        random_seed=42
    )

    # Print full summary
    print_summary(stats, num_simulations)

    # Additional analysis
    print("\n" + "=" * 60)
    print("ADDITIONAL STATISTICS")
    print("=" * 60)

    # Calculate min, max, median steps
    steps_per_sim = [len(history) for history in histories]
    steps_per_sim.sort()

    print(f"\nSteps to complete:")
    print(f"  Minimum: {min(steps_per_sim)}")
    print(f"  Maximum: {max(steps_per_sim)}")
    print(f"  Median: {steps_per_sim[len(steps_per_sim)//2]}")
    print(f"  Average: {sum(steps_per_sim) / len(steps_per_sim):.2f}")

    # Show quartiles
    q1_idx = len(steps_per_sim) // 4
    q3_idx = 3 * len(steps_per_sim) // 4
    print(f"  25th percentile: {steps_per_sim[q1_idx]}")
    print(f"  75th percentile: {steps_per_sim[q3_idx]}")

    # Find longest simulation
    longest_sim_idx = max(range(len(histories)), key=lambda i: len(histories[i]))
    print(f"\nLongest simulation (#{longest_sim_idx + 1}): {len(histories[longest_sim_idx])} steps")

    # Show first 10 steps of longest simulation
    print("First 10 steps:")
    for step_num, (from_lvl, to_lvl, trans_type) in enumerate(histories[longest_sim_idx][:10], 1):
        print(f"  Step {step_num}: Level {from_lvl} -> {to_lvl} ({trans_type})")
    if len(histories[longest_sim_idx]) > 10:
        print(f"  ... ({len(histories[longest_sim_idx]) - 10} more steps)")


if __name__ == "__main__":
    main()
