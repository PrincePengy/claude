#!/usr/bin/env python3
"""
Example usage of the probability transition simulator.
"""

from probability_transition_simulator import simulate_transitions, print_summary


# Example 1: Simple progression system (e.g., game leveling)
def example_simple():
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Simple Progression System")
    print("=" * 60)

    # Define probabilities for each level
    # Format: [P_success, P_break, P_fail, P_downgrade]
    transition_array = [
        [0.7, 0.1, 0.1, 0.1],   # Level 0: High success rate
        [0.6, 0.15, 0.15, 0.1], # Level 1
        [0.5, 0.2, 0.2, 0.1],   # Level 2
        [0.4, 0.2, 0.2, 0.2],   # Level 3: Lower success rate
        [0.3, 0.25, 0.25, 0.2], # Level 4
    ]

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=0,
        target_level=4,
        num_simulations=500,
        random_seed=123
    )

    print_summary(stats, num_simulations=500)


# Example 2: Equipment upgrade system
def example_equipment_upgrade():
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Equipment Upgrade System")
    print("=" * 60)
    print("Break = item breaks but stays same level")
    print("Fail = upgrade fails, item stays same level")
    print("")

    # Realistic equipment upgrade probabilities
    # Gets harder as you level up
    transition_array = [
        [0.95, 0.02, 0.03, 0.0],   # Level 0->1: Very easy
        [0.85, 0.05, 0.10, 0.0],   # Level 1->2: Easy
        [0.70, 0.10, 0.15, 0.05],  # Level 2->3: Medium
        [0.50, 0.15, 0.25, 0.10],  # Level 3->4: Hard
        [0.30, 0.25, 0.30, 0.15],  # Level 4->5: Very hard
        [0.15, 0.30, 0.40, 0.15],  # Level 5->6: Extreme
        [0.05, 0.35, 0.45, 0.15],  # Level 6->7: Nearly impossible
    ]

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=0,
        target_level=5,
        num_simulations=100,
        random_seed=456
    )

    print_summary(stats, num_simulations=100)

    # Show how many attempts each simulation took
    attempt_counts = [len(history) for history in histories]
    print(f"\nMin attempts: {min(attempt_counts)}")
    print(f"Max attempts: {max(attempt_counts)}")
    print(f"Median attempts: {sorted(attempt_counts)[len(attempt_counts)//2]}")


# Example 3: Detailed single simulation
def example_detailed_simulation():
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Detailed Single Simulation")
    print("=" * 60)

    transition_array = [
        [0.5, 0.2, 0.2, 0.1],  # Level 0
        [0.4, 0.25, 0.25, 0.1], # Level 1
        [0.3, 0.3, 0.3, 0.1],   # Level 2
    ]

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=0,
        target_level=2,
        num_simulations=1,
        verbose=True,  # This will print detailed step-by-step info
        random_seed=789
    )


# Example 4: Analyzing break vs fail events
def example_break_vs_fail_analysis():
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Break vs Fail Analysis")
    print("=" * 60)
    print("This example shows why distinguishing break and fail is important")
    print("")

    # High break probability
    transition_array = [
        [0.4, 0.4, 0.1, 0.1],  # Level 0: High break rate
        [0.4, 0.1, 0.4, 0.1],  # Level 1: High fail rate
        [0.4, 0.2, 0.2, 0.2],  # Level 2: Balanced
    ]

    stats, histories = simulate_transitions(
        transition_array=transition_array,
        start_level=0,
        target_level=2,
        num_simulations=1000,
        random_seed=999
    )

    print_summary(stats, num_simulations=1000)

    # Count breaks and fails by level
    level_0_breaks = sum(1 for hist in histories for from_lvl, to_lvl, trans in hist
                         if from_lvl == 0 and trans == 'break')
    level_0_fails = sum(1 for hist in histories for from_lvl, to_lvl, trans in hist
                        if from_lvl == 0 and trans == 'fail')
    level_1_breaks = sum(1 for hist in histories for from_lvl, to_lvl, trans in hist
                         if from_lvl == 1 and trans == 'break')
    level_1_fails = sum(1 for hist in histories for from_lvl, to_lvl, trans in hist
                        if from_lvl == 1 and trans == 'fail')

    print("\nDetailed Analysis:")
    print(f"Level 0 - Breaks: {level_0_breaks}, Fails: {level_0_fails}")
    print(f"Level 1 - Breaks: {level_1_breaks}, Fails: {level_1_fails}")
    print("\nNote: Level 0 has more breaks, Level 1 has more fails")
    print("This distinction could represent different game mechanics:")
    print("  - Break: Item damaged but can be repaired")
    print("  - Fail: Upgrade attempt simply failed, no damage")


if __name__ == "__main__":
    example_simple()
    example_equipment_upgrade()
    example_detailed_simulation()
    example_break_vs_fail_analysis()
