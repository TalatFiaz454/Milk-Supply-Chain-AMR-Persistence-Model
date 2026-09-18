import numpy as np
import matplotlib.pyplot as plt
from model_scen2 import BiofilmPersistenceABM

# -----------------------------
# Experiment settings
# -----------------------------

cleaning_intervals = [1, 3, 7, 14, 30]
N_STEPS = 150
STEADY_WINDOW = 30  # last N steps for steady-state averaging

# High AMR upstream input (from ABM-1-like distribution)
high_amr = [2, 3, 4] * 40

steady_state_results = {}

# -----------------------------
# Run experiments
# -----------------------------

for interval in cleaning_intervals:
    model = BiofilmPersistenceABM(
        upstream_amr_distribution=high_amr,
        cleaning_interval=interval,
        shedding_prob=0.25
    )

    for _ in range(N_STEPS):
        model.step()

    steady_state_amr = np.mean(model.mean_amr_history[-STEADY_WINDOW:])
    steady_state_results[interval] = steady_state_amr

# -----------------------------
# Print results
# -----------------------------

print("\nCleaning interval → steady-state biofilm AMR")
for interval, amr in steady_state_results.items():
    print(f"{interval:>3} steps : {amr:.3f}")


# -----------------------------
# Plot steady-state AMR vs cleaning interval
# -----------------------------

intervals = list(steady_state_results.keys())
amr_values = list(steady_state_results.values())

plt.figure(figsize=(6, 4))
plt.plot(intervals, amr_values, marker="o")
plt.xlabel("Cleaning interval (time steps)")
plt.ylabel("Steady-state mean biofilm AMR")
plt.title("Effect of cleaning frequency on AMR persistence (ABM-2)")
plt.grid(True)
plt.tight_layout()
plt.savefig("abm2_cleaning_threshold.png", dpi=300)
plt.close()

print("\nPlot saved as: abm2_cleaning_threshold.png")


# -----------------------------
# Threshold detection
# -----------------------------

AMR_THRESHOLD = 0.2

# Find smallest cleaning interval where persistence disappears
threshold_interval = None

for interval in sorted(steady_state_results.keys()):
    if steady_state_results[interval] < AMR_THRESHOLD:
        threshold_interval = interval
        break

print("\nPersistence threshold analysis")
print(f"AMR collapse threshold: {AMR_THRESHOLD}")

if threshold_interval is not None:
    print(
        f"Persistence disappears at cleaning interval ≤ {threshold_interval} time steps"
    )
else:
    print("Persistence persists at all tested cleaning intervals")
