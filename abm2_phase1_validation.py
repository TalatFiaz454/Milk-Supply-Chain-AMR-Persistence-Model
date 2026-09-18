import numpy as np
import matplotlib.pyplot as plt
from model_scen2 import BiofilmPersistenceABM

# ======================================
# COMMON SETTINGS
# ======================================

HIGH_AMR = [3,4,3,4,3]*40
LOW_AMR = [0,1,0,1]*60

T_SWITCH = 40
TOTAL_STEPS = 120

# ======================================
# PANEL A — MEMORY TEST
# ======================================

def run_memory_experiment():

    model = BiofilmPersistenceABM(
        upstream_amr_distribution=HIGH_AMR,
        cleaning_interval=7
    )

    history = []
    input_track = []

    for t in range(TOTAL_STEPS):

        if t == T_SWITCH:
            model.set_upstream_distribution(LOW_AMR)

        model.step()
        history.append(model.mean_amr_history[-1])

        input_track.append(
            np.mean(model.upstream_amr_distribution)
        )

    return history, input_track

# ======================================
# PANEL B — CLEANING THRESHOLD
# ======================================

def run_cleaning_threshold():

    intervals = [1,3,7,14,30]
    steady_means = []

    for interval in intervals:

        model = BiofilmPersistenceABM(
            upstream_amr_distribution=HIGH_AMR,
            cleaning_interval=interval
        )

        for _ in range(TOTAL_STEPS):
            model.step()

        steady = np.mean(model.mean_amr_history[-30:])
        steady_means.append(steady)

    return intervals, steady_means

# ======================================
# PANEL C — MECHANISM REMOVAL
# ======================================

def run_removal_tests():

    tests = {
        "Baseline": {},
        "No Colonization": {"disable_colonization": True},
        "No Growth": {"disable_growth": True},
        "No Surfaces": {"disable_surfaces": True}
    }

    results = {}

    for name, params in tests.items():

        model = BiofilmPersistenceABM(
            upstream_amr_distribution=HIGH_AMR,
            cleaning_interval=7,
            **params
        )

        hist = []

        for _ in range(TOTAL_STEPS):
            model.step()
            hist.append(model.mean_amr_history[-1])

        results[name] = hist

    return results

# ======================================
# RUN ALL EXPERIMENTS
# ======================================

mem_hist, mem_input = run_memory_experiment()
intervals, threshold_vals = run_cleaning_threshold()
removal_results = run_removal_tests()

# ======================================
# CREATE MULTI PANEL FIGURE
# ======================================

fig, axes = plt.subplots(1,3, figsize=(18,5))

# ----- PANEL A -----
ax = axes[0]
ax.plot(mem_hist, label="Biofilm AMR")
ax.plot(mem_input, linestyle="--", label="Upstream AMR")
ax.axvline(T_SWITCH, linestyle=":")
ax.set_title("A. Memory Test")
ax.set_xlabel("Time")
ax.set_ylabel("Mean AMR")
ax.legend()

# ----- PANEL B -----
ax = axes[1]
ax.plot(intervals, threshold_vals, marker="o")
ax.set_title("B. Cleaning Threshold")
ax.set_xlabel("Cleaning Interval")
ax.set_ylabel("Steady Biofilm AMR")

# ----- PANEL C -----
ax = axes[2]
for name, hist in removal_results.items():
    ax.plot(hist, label=name)
ax.set_title("C. Mechanism Removal")
ax.set_xlabel("Time")
ax.set_ylabel("Mean Biofilm AMR")
ax.legend()

plt.tight_layout()
plt.savefig("FIG_ABM2_Mechanistic_Validation.png", dpi=300)
plt.show()
