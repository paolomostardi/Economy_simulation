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


@dataclass
class SpendingPolicy:
    """Represents spending policy as array of 4 values summing to 100."""
    military: float
    healthcare: float
    education: float
    research_and_infrastructure: float
    
    def __post_init__(self):
        """Ensure values sum to 100."""
        total = self.military + self.healthcare + self.education + self.research_and_infrastructure
        if total > 0:
            self.military = (self.military / total) * 100
            self.healthcare = (self.healthcare / total) * 100
            self.education = (self.education / total) * 100
            self.research_and_infrastructure = (self.research_and_infrastructure / total) * 100
    
    def to_budget_allocation(self, research_ratio: float = 0.5) -> BudgetAllocation:
        """Convert spending policy to detailed budget allocation.
        
        Args:
            research_ratio: How much of research_and_infrastructure goes to research (0-1).
                           Rest goes to infrastructure.
        """
        research_ratio = max(0, min(1, research_ratio))
        research_and_infra_total = self.research_and_infrastructure / 100
        
        return BudgetAllocation(
            military=self.military / 100,
            healthcare=self.healthcare / 100,
            education=self.education / 100,
            research=research_and_infra_total * research_ratio,
            infrastructure=research_and_infra_total * (1 - research_ratio)
        )


class Economy:
    """Manages economic indicators and budget."""
    
    def __init__(self, population: int, stability: float, technology: float,
                 corruption: float, democracy_index: float, age_groups: dict = None):
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
        
        # Calculate spending policy and budget allocation
        self.spending_policy = self.calculate_spending_policy(
            democracy_index, age_groups
        )
        self.budget = self.spending_policy.to_budget_allocation()
        
        # Budget spending (absolute values)
        self.healthcare_spending = 0.0
        self.education_spending = 0.0
        self.research_spending = 0.0
        self.military_spending = 0.0
        self.infrastructure_spending = 0.0
    
    def calculate_spending_policy(self, democracy_index: float, age_groups: dict = None) -> SpendingPolicy:
        """Calculate spending policy based on democracy index and age distribution.
        
        Args:
            democracy_index: Country's democracy index (0-100)
            age_groups: Dictionary of age groups with population counts
        
        Returns:
            SpendingPolicy with 4 categories summing to 100
        """
        # Start with base allocation (25% each)
        base_military = 25.0
        base_healthcare = 25.0
        base_education = 25.0
        base_research_and_infra = 25.0
        
        # Random factor for each country (±10% variation)
        random_military = random.uniform(-10, 10)
        random_healthcare = random.uniform(-10, 10)
        random_education = random.uniform(-10, 10)
        random_research = random.uniform(-10, 10)
        
        # Democracy effect: more democratic countries spend less on military
        democracy_factor = (100 - democracy_index) / 100
        military_adjustment = democracy_factor * 15  # Up to 15% more for authoritarian states
        
        # Age distribution effect: older populations need more healthcare
        elderly_percentage = 0.0
        if age_groups:
            total_pop = sum(group.population for group in age_groups.values())
            if total_pop > 0:
                elderly_pop = age_groups.get("elderly", type('obj', (object,), {'population': 0})()).population
                elderly_percentage = elderly_pop / total_pop
        
        healthcare_adjustment = elderly_percentage * 20  # Up to 20% more for aging populations
        
        # Apply adjustments
        military = base_military + random_military + military_adjustment
        healthcare = base_healthcare + random_healthcare + healthcare_adjustment
        education = base_education + random_education
        research_and_infra = base_research_and_infra + random_research
        
        # Ensure all values are positive
        military = max(5, military)
        healthcare = max(5, healthcare)
        education = max(5, education)
        research_and_infra = max(5, research_and_infra)
        
        return SpendingPolicy(
            military=military,
            healthcare=healthcare,
            education=education,
            research_and_infrastructure=research_and_infra
        )
    
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
                     corruption: float, democracy_index: float, age_groups: dict = None,
                     agriculture_penalty: float = 0, resource_penalty: float = 0):
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
        
        # Recalculate spending policy based on current conditions
        self.spending_policy = self.calculate_spending_policy(democracy_index, age_groups)
        self.budget = self.spending_policy.to_budget_allocation()
        
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
