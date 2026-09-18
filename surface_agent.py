from mesa import Agent
import random


class SurfaceAgent(Agent):
    """
    Represents a milk-contact surface with biofilm-mediated AMR persistence
    """

    def __init__(
        self,
        model,
        initial_biomass=0.0,
        initial_amr=0.0
    ):
        super().__init__(model)

        self.biofilm_biomass = initial_biomass
        self.mean_amr = initial_amr
        self.biofilm_age = 0
        self.last_cleaned = 0

    # -----------------------------
    # Core processes
    # -----------------------------

    def colonize(self, milk_amr):
        """Milk-to-surface colonization"""
        if random.random() < self.model.colonization_prob:
            added_mass = self.model.colonization_mass
            self.mean_amr = (
                (self.mean_amr * self.biofilm_biomass +
                 milk_amr * added_mass) /
                (self.biofilm_biomass + added_mass + 1e-9)
            )
            self.biofilm_biomass += added_mass

    def grow(self):
        """Slow biofilm growth"""
        self.biofilm_biomass *= (1 + self.model.biofilm_growth_rate)
        self.biofilm_age += 1

    def shed(self):
        """Shedding back into milk"""
        if self.biofilm_biomass <= 0:
            return None

        if random.random() < self.model.shedding_prob:
            shed_mass = self.biofilm_biomass * self.model.shedding_fraction
            self.biofilm_biomass -= shed_mass
            return self.mean_amr

        return None

    def clean(self):
        """Imperfect cleaning event"""
        if random.random() < self.model.cleaning_efficiency:
            self.biofilm_biomass *= (1 - self.model.cleaning_strength)
            self.last_cleaned = 0
            if self.biofilm_biomass < 1e-3:
                self.biofilm_biomass = 0.0
                self.mean_amr = 0.0

    # -----------------------------
    # Agent step
    # -----------------------------

    def step(self):
        # Sample AMR from ABM-1 output distribution
        milk_amr = self.model.sample_upstream_amr()

        # Colonization from milk
        self.colonize(milk_amr)

        # Biofilm growth
        self.grow()

        # Shedding (for diagnostics)
        self.shed()

        # Cleaning events
        if self.model.current_step % self.model.cleaning_interval == 0:
            self.clean()

        self.last_cleaned += 1
