"""
Economy system - handles GDP, taxes, budget, and employment.
"""

import random
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from resources import NaturalResources
    from country import BudgetAllocation


class Economy:
    """Manages economic indicators and budget."""
    
    def __init__(self, population: int, stability: float, technology: float,
                 corruption: float, democracy_index: float):
        self.gdp = self._generate_gdp(population, stability, technology)
        self.gdp_per_capita = self.gdp / population
        self.gdp_growth_rate = random.uniform(-0.02, 0.05)
        self.inflation = random.uniform(0.01, 0.05)
        self.tax_rate = random.uniform(10, 50)
        
        self.government_revenue = self.gdp * (self.tax_rate / 100)
        self.effective_revenue = self.government_revenue * (1 - corruption / 100)
        
        self.unemployment_rate = self._generate_unemployment(stability, technology)
        self.inequality_factor = random.uniform(0.2, 0.8)
        
        # Budget spending (absolute values)
        self.healthcare_spending = 0.0
        self.education_spending = 0.0
        self.research_spending = 0.0
        self.military_spending = 0.0
        self.infrastructure_spending = 0.0
    
    def _generate_gdp(self, population: int, stability: float, technology: float) -> float:
        """Generate initial GDP based on population, stability, and technology."""
        # Base GDP per capita varies widely
        base_gdp_per_capita = random.uniform(2000, 50000)
        
        # Adjust by stability and technology
        stability_factor = stability / 100
        tech_factor = technology / 100
        
        gdp_per_capita = base_gdp_per_capita * stability_factor * tech_factor
        gdp = gdp_per_capita * population
        
        return gdp
    
    def _generate_unemployment(self, stability: float, technology: float) -> float:
        """Generate initial unemployment rate."""
        base_unemployment = random.uniform(2, 25)
        
        # Adjust by stability and technology
        stability_penalty = (100 - stability) / 100 * 5
        tech_benefit = technology / 100 * 3
        
        unemployment = base_unemployment + stability_penalty - tech_benefit
        return max(0, min(40, unemployment))
    
    def yearly_update(self, population: int, stability: float, technology: float,
                     corruption: float, democracy_index: float, budget: 'BudgetAllocation',
                     resources: 'NaturalResources'):
        """Update economy for one year."""
        # Update GDP based on growth rate
        self.gdp *= (1 + self.gdp_growth_rate)
        
        # Recalculate GDP per capita
        self.gdp_per_capita = self.gdp / population if population > 0 else 0
        
        # Update growth rate based on factors
        self._update_growth_rate(stability, technology, self.unemployment_rate, corruption)
        
        # Update inflation
        self._update_inflation()
        
        # Recalculate government revenue
        self.government_revenue = self.gdp * (self.tax_rate / 100)
        self.effective_revenue = self.government_revenue * (1 - corruption / 100)
        
        # Allocate budget spending
        self._allocate_budget_spending(budget)
        
        # Update unemployment
        self._update_unemployment(stability, technology, self.gdp_growth_rate)
        
        # Update inequality
        self._update_inequality(stability, democracy_index)
    
    def _update_growth_rate(self, stability: float, technology: float, unemployment: float, corruption: float):
        """Update GDP growth rate based on economic factors."""
        # Base growth
        base_growth = random.uniform(-0.01, 0.04)
        
        # Stability bonus
        stability_bonus = (stability / 100 - 0.5) * 0.05
        
        # Technology bonus
        tech_bonus = (technology / 100) * 0.02
        
        # Unemployment penalty
        unemployment_penalty = (unemployment / 40) * 0.03
        
        # Corruption penalty
        corruption_penalty = (corruption / 100) * 0.02
        
        # Resource extraction bonus
        resource_bonus = 0.005  # Placeholder, would be calculated from actual resources
        
        new_growth = (base_growth + stability_bonus + tech_bonus + resource_bonus
                     - unemployment_penalty - corruption_penalty)
        
        # Smooth transition
        self.gdp_growth_rate = self.gdp_growth_rate * 0.7 + new_growth * 0.3
        self.gdp_growth_rate = max(-0.1, min(0.15, self.gdp_growth_rate))
    
    def _update_inflation(self):
        """Update inflation rate."""
        # Inflation tends to revert to target (2%)
        target = 0.02
        adjustment = (target - self.inflation) * 0.1
        fluctuation = random.uniform(-0.01, 0.01)
        
        self.inflation = max(0, min(0.2, self.inflation + adjustment + fluctuation))
    
    def _allocate_budget_spending(self, budget: 'BudgetAllocation'):
        """Calculate absolute spending amounts from budget percentages."""
        self.healthcare_spending = self.effective_revenue * budget.healthcare
        self.education_spending = self.effective_revenue * budget.education
        self.research_spending = self.effective_revenue * budget.research
        self.military_spending = self.effective_revenue * budget.military
        self.infrastructure_spending = self.effective_revenue * budget.infrastructure
    
    def _update_unemployment(self, stability: float, technology: float, gdp_growth: float):
        """Update unemployment rate."""
        # GDP growth reduces unemployment
        growth_effect = -gdp_growth * 0.5
        
        # Stability effect
        stability_effect = (stability / 100 - 0.5) * -2
        
        # Technology effect (can increase structural unemployment)
        tech_effect = (technology / 100) * 0.5
        
        # Random fluctuation
        fluctuation = random.uniform(-0.5, 0.5)
        
        change = growth_effect + stability_effect + tech_effect + fluctuation
        self.unemployment_rate = max(0, min(40, self.unemployment_rate + change))
    
    def _update_inequality(self, stability: float, democracy_index: float):
        """Update inequality factor."""
        # Low stability increases inequality
        stability_effect = (1 - stability / 100) * 0.02
        
        # Low democracy increases inequality
        democracy_effect = (1 - democracy_index / 100) * 0.01
        
        # Random fluctuation
        fluctuation = random.uniform(-0.01, 0.01)
        
        change = stability_effect + democracy_effect + fluctuation
        self.inequality_factor = max(0, min(1, self.inequality_factor + change))
