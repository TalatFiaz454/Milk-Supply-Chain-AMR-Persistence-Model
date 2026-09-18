from mesa import Model
from mesa.time import RandomActivation
from surface_agent import SurfaceAgent
import numpy as np
import random


class BiofilmPersistenceABM(Model):
    """
    ABM-2: Biofilm-mediated persistence of AMR
    """

    def __init__(
        self,
        upstream_amr_distribution,
        n_surfaces=10,
        colonization_prob=0.3,
        colonization_mass=0.5,
        biofilm_growth_rate=0.05,
        shedding_prob=0.2,
        shedding_fraction=0.1,
        cleaning_interval=7,
        cleaning_efficiency=0.8,
        cleaning_strength=0.7,
        seed=None
    ):
        super().__init__(seed=seed)

        self.schedule = RandomActivation(self)

        # -----------------------------
        # Parameters
        # -----------------------------

        self.upstream_amr_distribution = upstream_amr_distribution

        self.colonization_prob = colonization_prob
        self.colonization_mass = colonization_mass
        self.biofilm_growth_rate = biofilm_growth_rate
        self.shedding_prob = shedding_prob
        self.shedding_fraction = shedding_fraction

        self.cleaning_interval = cleaning_interval
        self.cleaning_efficiency = cleaning_efficiency
        self.cleaning_strength = cleaning_strength

        self.current_step = 0

        # -----------------------------
        # Create surface agents
        # -----------------------------

        for _ in range(n_surfaces):
            agent = SurfaceAgent(self)
            self.schedule.add(agent)

        # -----------------------------
        # Data storage
        # -----------------------------

        self.mean_amr_history = []
        self.total_biomass_history = []

    # -----------------------------
    # Sampling from ABM-1 outputs
    # -----------------------------

    def sample_upstream_amr(self):
        return random.choice(self.upstream_amr_distribution)
    # -----------------------------
    # Model step
    # -----------------------------

    def step(self):
        self.current_step += 1
        self.schedule.step()

        # Record outputs
        mean_amr = np.mean(
            [a.mean_amr for a in self.schedule.agents if a.biofilm_biomass > 0]
            or [0]
        )
        total_biomass = np.sum(
            [a.biofilm_biomass for a in self.schedule.agents]
        )

        self.mean_amr_history.append(mean_amr)
        self.total_biomass_history.append(total_biomass)
