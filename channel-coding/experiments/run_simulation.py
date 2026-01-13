"""
Run experiments for Slotted Aloha simulation.

This script evaluates system throughput as a function of:
- number of active users
- maximum backoff window size

Results are plotted for comparative analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from tqdm import tqdm


# =========================
# Core simulation entities
# =========================

@dataclass
class User:
    counter: int = 0  # slots remaining until next transmission attempt

    def tick(self) -> None:
        if self.counter > 0:
            self.counter -= 1

    def reschedule(self, max_backoff: int, rng: np.random.Generator) -> None:
        self.counter = int(rng.integers(0, max_backoff + 1))


def simulate_slotted_aloha(
    n_users: int,
    num_slots: int,
    max_backoff: int,
    seed: int
) -> float:
    """
    Simulate Slotted Aloha for a fixed number of users.

    Returns:
        Throughput (successful transmissions per slot)
    """
    rng = np.random.default_rng(seed)

    users = [User() for _ in range(n_users)]
    for u in users:
        u.reschedule(max_backoff, rng)

    successful_slots = 0

    for _ in range(num_slots):
        for u in users:
            u.tick()

        transmitting = [u for u in users if u.counter == 0]

        if len(transmitting) == 1:
            successful_slots += 1
            transmitting[0].reschedule(max_backoff, rng)
        elif len(transmitting) > 1:
            for u in transmitting:
                u.reschedule(max_backoff, rng)

    return successful_slots / num_slots


# =========================
# Experiment runner
# =========================

def run_experiment(
    n_max: int,
    num_slots: int,
    backoff_sizes: list[int],
    base_seed: int = 0
) -> dict[int, list[float]]:
    """
    Run throughput experiments for different backoff window sizes.
    """
    results = {m: [] for m in backoff_sizes}

    for m in backoff_sizes:
        for n in tqdm(range(n_max), desc=f"max_backoff={m}"):
            seed = base_seed + 100_000 * m + n
            thr = simulate_slotted_aloha(
                n_users=n,
                num_slots=num_slots,
                max_backoff=m,
                seed=seed
            )
            results[m].append(thr)

    return results


# =========================
# Plotting
# =========================

def plot_results(results: dict[int, list[float]], title: str) -> None:
    ns = np.arange(len(next(iter(results.values()))))

    plt.figure(figsize=(9, 5))
    for m, thr in results.items():
        plt.plot(ns, thr, label=f"max_backoff={m}")

    plt.xlabel("Number of users (n)")
    plt.ylabel("Throughput (packets / slot)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


# =========================
# Main execution
# =========================

if __name__ == "__main__":

    # Low-load regime
    results_low = run_experiment(
        n_max=4,
        num_slots=1_000,
        backoff_sizes=[8, 16, 32],
        base_seed=42
    )
    plot_results(results_low, "Slotted Aloha Throughput (Low Load)")

    # High-load regime
    results_high = run_experiment(
        n_max=65,
        num_slots=50_000,
        backoff_sizes=[8, 16, 32, 64, 128],
        base_seed=42
    )
    plot_results(results_high, "Slotted Aloha Throughput (High Load)")
