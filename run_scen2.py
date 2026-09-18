# STEP 1 — High → Low AMR input switch experiment (MEMORY TEST)
# 1️⃣ Scientific question
#
# Does biofilm AMR persist after upstream AMR input drops?
#
# This tests system memory, which is the raison d’être of ABM-2.
#
# 2️⃣ Experimental design (what you will do)
#
# You divide the simulation into two phases:
#
# Phase	Time steps	Upstream AMR input
# Phase 1	0–T₁	High AMR
# Phase 2	T₁–T₂	Low AMR
#
# Everything else stays identical.

from model_scen2 import BiofilmPersistenceABM
import matplotlib.pyplot as plt

# -----------------------------
# Define AMR input distributions
# -----------------------------

high_amr = [2, 3, 4] * 40
low_amr = [0, 1] * 60

# -----------------------------
# Initialize model
# -----------------------------

model = BiofilmPersistenceABM(
    upstream_amr_distribution=high_amr,
    cleaning_interval=7,   # keep fixed
    shedding_prob=0.25
)

T1 = 40    # switch point
T2 = 120   # total time

biofilm_amr = []
input_amr = []

# -----------------------------
# Run simulation
# -----------------------------

for t in range(T2):
    if t == T1:
        model.set_upstream_distribution(low_amr)

    model.step()

    biofilm_amr.append(model.mean_amr_history[-1])
    input_amr.append(
        sum(model.upstream_amr_distribution) /
        len(model.upstream_amr_distribution)
    )

# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(10, 4))
plt.plot(biofilm_amr, label="Biofilm AMR")
plt.plot(input_amr, linestyle="--", label="Upstream AMR")
plt.axvline(T1, color="red", linestyle=":", label="Input switch")
plt.xlabel("Time")
plt.ylabel("Mean AMR genes")
plt.legend()
plt.tight_layout()
plt.savefig("abm2_memory_experiment.png", dpi=300)
plt.close()
