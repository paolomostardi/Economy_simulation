"""
Economy system - handles GDP, taxes, budget, and employment.
"""
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from population import Population
    from industries import Industries


@dataclass
class BudgetAllocation:
    """Represents budget allocation percentages."""
    military: float
    healthcare: float
    education: float
    research: float
    infrastructure: float


class Economy:
    """Manages economic indicators and budget."""
    
    def __init__(self, population: int, stability: float, technology: float,
                 corruption: float, democracy_index: float):
        self.gdp = self._generate_gdp(population, stability, technology)
        self.previous_gdp = self.gdp
        self.gdp_per_capita = self.gdp / population if population > 0 else 0
        self.gdp_growth_rate = random.uniform(-0.02, 0.05)
        self.inflation = random.uniform(0.01, 0.05)
        self.tax_rate = random.uniform(10, 50)
        
        self.government_revenue = self.gdp * (self.tax_rate / 100)
        self.effective_revenue = self.government_revenue * (1 - corruption / 100)
        
        self.unemployment_rate = self._generate_unemployment(stability, technology)
        self.inequality_factor = random.uniform(0.2, 0.8)
        
        # Budget allocation (percentages)
        self.budget = BudgetAllocation(
            military=random.uniform(0.1, 0.3),
            healthcare=random.uniform(0.15, 0.35),
            education=random.uniform(0.1, 0.25),
            research=random.uniform(0.05, 0.15),
            infrastructure=random.uniform(0.1, 0.25)
        )
        
        # Normalize budget to sum to 1
        total = (self.budget.military + self.budget.healthcare + self.budget.education +
                self.budget.research + self.budget.infrastructure)
        self.budget.military /= total
        self.budget.healthcare /= total
        self.budget.education /= total
        self.budget.research /= total
        self.budget.infrastructure /= total
        
        # Budget spending (absolute values)
        self.healthcare_spending = 0.0
        self.education_spending = 0.0
        self.research_spending = 0.0
        self.military_spending = 0.0
        self.infrastructure_spending = 0.0
    
    def _generate_gdp(self, population: int, stability: float, technology: float) -> float:
        """Generate initial GDP based on population, stability, and technology."""
        base_gdp_per_capita = random.uniform(2000, 50000)
        stability_factor = stability / 100
        tech_factor = technology / 100
        
        gdp_per_capita = base_gdp_per_capita * stability_factor * tech_factor
        return gdp_per_capita * population
    
    def _generate_unemployment(self, stability: float, technology: float) -> float:
        """Generate initial unemployment rate."""
        base_unemployment = random.uniform(2, 25)
        stability_penalty = (100 - stability) / 100 * 5
        tech_benefit = technology / 100 * 3
        
        unemployment = base_unemployment + stability_penalty - tech_benefit
        return max(0, min(40, unemployment))
    
    def update_from_industries(self, industries: 'Industries'):
        """Update GDP based on industry outputs."""
        self.previous_gdp = self.gdp
        self.gdp = industries.get_total_gdp()
        
        # Calculate growth rate
        if self.previous_gdp > 0:
            self.gdp_growth_rate = (self.gdp - self.previous_gdp) / self.previous_gdp
        else:
            self.gdp_growth_rate = 0.0
    
    def yearly_update(self, population: int, stability: float, technology: float,
                     corruption: float, democracy_index: float, budget: BudgetAllocation,
                     agriculture_penalty: float, resource_penalty: float):
        """Update economy for one year."""
        # Recalculate GDP per capita
        self.gdp_per_capita = self.gdp / population if population > 0 else 0
        
        # Update inflation (affected by food shortages)
        base_inflation = 0.02
        shortage_effect = 10 * (1 - agriculture_penalty) if agriculture_penalty > 0 else 0
        self.inflation = max(0, min(0.2, base_inflation + shortage_effect * 0.01 + random.uniform(-0.01, 0.01)))
        
        # Recalculate government revenue
        self.government_revenue = self.gdp * (self.tax_rate / 100)
        self.effective_revenue = self.government_revenue * (1 - corruption / 100)
        
        # Update budget allocation
        self.budget = budget
        
        # Calculate absolute spending
        self.healthcare_spending = self.effective_revenue * self.budget.healthcare
        self.education_spending = self.effective_revenue * self.budget.education
        self.research_spending = self.effective_revenue * self.budget.research
        self.military_spending = self.effective_revenue * self.budget.military
        self.infrastructure_spending = self.effective_revenue * self.budget.infrastructure
        
        # Update unemployment based on GDP growth
        growth_effect = -self.gdp_growth_rate * 0.5
        stability_effect = (stability / 100 - 0.5) * -2
        tech_effect = (technology / 100) * 0.5
        fluctuation = random.uniform(-0.5, 0.5)
        
        change = growth_effect + stability_effect + tech_effect + fluctuation
        self.unemployment_rate = max(0, min(40, self.unemployment_rate + change))
        
        # Update inequality
        stability_effect = (1 - stability / 100) * 0.02
        democracy_effect = (1 - democracy_index / 100) * 0.01
        fluctuation = random.uniform(-0.01, 0.01)
        
        change = stability_effect + democracy_effect + fluctuation
        self.inequality_factor = max(0, min(1, self.inequality_factor + change))
        
        # Tax rate may change slightly
        self.tax_rate = max(10, min(50, self.tax_rate + random.uniform(-1, 1)))
