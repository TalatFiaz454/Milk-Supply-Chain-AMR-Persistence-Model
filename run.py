from model import BiofilmPersistenceABM
import matplotlib.pyplot as plt

# -----------------------------
# Example ABM-1 output (sampled)
# -----------------------------

# This would come from ABM-1 get_outputs()
upstream_amr = (
    [0, 1, 2] * 40 +
    [3] * 15 +
    [4] * 5
)

# -----------------------------
# Run ABM-2
# -----------------------------

model = BiofilmPersistenceABM(
    upstream_amr_distribution=upstream_amr,
    n_surfaces=15,
    cleaning_interval=7,
    shedding_prob=0.25
)

N_STEPS = 120  # ~4 months

for _ in range(N_STEPS):
    model.step()

# -----------------------------
# Plot results
# -----------------------------

plt.figure(figsize=(10, 4))
plt.plot(model.mean_amr_history, label="Mean biofilm AMR")
plt.xlabel("Time")
plt.ylabel("Mean AMR genes")
plt.title("Biofilm-mediated AMR persistence (ABM-2)")
plt.legend()
plt.tight_layout()
plt.savefig("abm2_biofilm_persistence.png", dpi=300)
plt.close()

