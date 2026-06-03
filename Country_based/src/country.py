"""
Country class - main entity in the simulation.
"""

import random
import math
from typing import Dict, List
from dataclasses import dataclass

from population import Population
from economy import Economy
from resources import NaturalResources
from culture import Culture
from geography import Geography


@dataclass
class BudgetAllocation:
    """Budget allocation percentages."""
    military: float = 0.0
    healthcare: float = 0.0
    education: float = 0.0
    research: float = 0.0
    infrastructure: float = 0.0


class Country:
    """Represents a country in the simulation."""
    
    def __init__(self, name: str):
        self.name = name
        
        # Basic properties
        self.stability: float = self._generate_stability()
        self.technology: float = random.uniform(20, 80)
        self.corruption: float = self._generate_corruption()
        self.democracy_index: float = self._generate_democracy_index()
        
        # Geography
        self.geography = Geography()
        
        # Population (generate first to calculate area based on population)
        self.population = Population(0, self.stability, self.technology)
        
        # Area (now can be based on population)
        self.area = self._generate_area()
        
        # Economy
        self.economy = Economy(
            self.population.total,
            self.stability,
            self.technology,
            self.corruption,
            self.democracy_index
        )
        
        # Resources
        self.resources = NaturalResources(self.area, self.geography)
        
        # Culture
        self.culture = Culture()
        
        # Budget allocation
        self.budget = BudgetAllocation()
        self._allocate_budget()
    
    def _generate_stability(self) -> float:
        """Generate initial stability score."""
        return random.uniform(30, 80)
    
    def _generate_corruption(self) -> float:
        """Generate corruption level using the specified formula."""
        if random.uniform(0, 1) < 0.4:
            # Uniform distribution between 15 and 30 (40% probability)
            return random.uniform(15, 30)
        else:
            if random.uniform(0, 1) < 0.4:
                # Logarithmic distribution from 15 down to 0 (24% probability)
                return 15 * math.exp(-random.uniform(0, 3))
            else:
                # Logarithmic distribution from 30 up to 100 (36% probability)
                return 30 + 70 * (1 - math.exp(-random.uniform(0, 3)))
    
    def _generate_democracy_index(self) -> float:
        """Generate democracy index."""
        return random.uniform(20, 90)
    
    def _generate_area(self) -> float:
        """Generate land area based on population."""
        # Area scales with population but with variation
        pop_factor = math.log(self.population.total) / math.log(500000000)
        base_area = 10000 + pop_factor * 1000000
        return random.uniform(base_area * 0.5, base_area * 2.0)
    
    def _allocate_budget(self):
        """Allocate budget across categories based on country priorities."""
        # Base allocations
        self.budget.military = random.uniform(0.05, 0.20)
        self.budget.healthcare = random.uniform(0.10, 0.25)
        self.budget.education = random.uniform(0.10, 0.25)
        self.budget.research = random.uniform(0.02, 0.10)
        self.budget.infrastructure = random.uniform(0.05, 0.20)
        
        # Adjust based on democracy
        if self.democracy_index > 70:
            self.budget.healthcare += 0.05
            self.budget.education += 0.05
            self.budget.military -= 0.05
        elif self.democracy_index < 30:
            self.budget.military += 0.10
            self.budget.healthcare -= 0.05
            self.budget.education -= 0.05
        
        # Normalize to ensure sum is reasonable
        total = sum([self.budget.military, self.budget.healthcare, self.budget.education,
                     self.budget.research, self.budget.infrastructure])
        if total > 0.8:
            scale = 0.8 / total
            self.budget.military *= scale
            self.budget.healthcare *= scale
            self.budget.education *= scale
            self.budget.research *= scale
            self.budget.infrastructure *= scale
    
    def yearly_update(self):
        """Update all country properties for one year."""
        # Update population
        self.population.yearly_update(
            self.economy.gdp_per_capita,
            self.stability,
            self.corruption,
            self.economy.unemployment_rate,
            self.economy.healthcare_spending,
            self.technology
        )
        
        # Update economy
        self.economy.yearly_update(
            self.population.total,
            self.stability,
            self.technology,
            self.corruption,
            self.democracy_index,
            self.budget,
            self.resources
        )
        
        # Update stability
        self._update_stability()
        
        # Update democracy
        self._update_democracy()
        
        # Update corruption
        self._update_corruption()
        
        # Update technology
        self._update_technology()
        
        # Update education
        self._update_education()
        
        # Update resources
        self.resources.yearly_extract()
        
        # Reallocate budget based on new conditions
        self._allocate_budget()
    
    def _update_stability(self):
        """Update stability based on various factors."""
        education_bonus = self.culture.technical_education / 100 * 2
        healthcare_bonus = (self.economy.healthcare_spending / self.economy.effective_revenue) * 2 if self.economy.effective_revenue > 0 else 0
        infrastructure_bonus = (self.budget.infrastructure) * 2
        gdp_growth_bonus = max(0, self.economy.gdp_growth_rate) * 5
        
        corruption_penalty = self.corruption / 100 * 3
        unemployment_penalty = self.economy.unemployment_rate / 40 * 3
        inequality_penalty = self.economy.inequality_factor * 3
        
        stability_change = (
            education_bonus + healthcare_bonus + infrastructure_bonus + gdp_growth_bonus
        ) - (corruption_penalty + unemployment_penalty + inequality_penalty)
        
        self.stability = max(0, min(100, self.stability + stability_change))
    
    def _update_democracy(self):
        """Update democracy index."""
        cultural_education = self.culture.cultural_education
        transparency_bonus = (100 - self.corruption) / 200
        corruption_penalty = self.corruption / 100
        instability_penalty = (100 - self.stability) / 200
        
        democracy_change = (cultural_education / 100 + transparency_bonus) - (corruption_penalty + instability_penalty)
        
        self.democracy_index = max(0, min(100, self.democracy_index + democracy_change))
    
    def _update_corruption(self):
        """Update corruption based on democracy and stability."""
        # Democracy reduces corruption
        corruption_modifier = 1 - self.democracy_index / 200
        
        # Stability also affects corruption
        stability_modifier = 1 - self.stability / 300
        
        # Small random fluctuation
        fluctuation = random.uniform(-1, 1)
        
        target_corruption = self.corruption * corruption_modifier * stability_modifier + fluctuation
        self.corruption = max(0, min(100, target_corruption))
    
    def _update_technology(self):
        """Update technology level based on research spending."""
        research_spending = self.budget.research * self.economy.effective_revenue
        tech_growth = (research_spending / self.economy.gdp) * 10 if self.economy.gdp > 0 else 0
        tech_growth += random.uniform(-0.5, 1.0)
        
        self.technology = max(0, min(100, self.technology + tech_growth))
    
    def _update_education(self):
        """Update education scores based on spending."""
        education_spending = self.budget.education * self.economy.effective_revenue
        tech_ed_growth = (education_spending / self.economy.gdp) * 5 if self.economy.gdp > 0 else 0
        cultural_ed_growth = tech_ed_growth * 0.8
        
        self.culture.technical_education = max(0, min(100, self.culture.technical_education + tech_ed_growth))
        self.culture.cultural_education = max(0, min(100, self.culture.cultural_education + cultural_ed_growth))
    
    def get_summary(self) -> Dict:
        """Get a summary of country statistics."""
        return {
            "name": self.name,
            "population": self.population.total,
            "gdp": self.economy.gdp,
            "gdp_per_capita": self.economy.gdp_per_capita,
            "stability": self.stability,
            "democracy": self.democracy_index,
            "corruption": self.corruption,
            "technology": self.technology,
            "inequality": self.economy.inequality_factor,
            "unemployment": self.economy.unemployment_rate
        }
