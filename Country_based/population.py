"""
Population management - Handles population generation, age distribution, and wealth classes.
"""
import random
import math
from typing import Dict
from dataclasses import dataclass


@dataclass
class AgeGroup:
    """Represents an age group in the population."""
    name: str
    min_age: int
    max_age: int
    population: int


@dataclass
class EconomicClass:
    """Represents an economic class in the population."""
    name: str
    population_percentage: float
    wealth_percentage: float


class PopulationManager:
    """Manages population-related properties and calculations."""
    
    def __init__(self):
        self.total_population: int = 0
        self.age_groups: Dict[str, AgeGroup] = {}
        self.economic_classes: Dict[str, EconomicClass] = {}
        self.disparity_factor: float = 0.0  # 0.0 to 1.0, inequality level
        self.education_technical: float = 0.0  # 0 to 100
        self.education_cultural: float = 0.0  # 0 to 100
    
    def generate_population(self):
        """Generate population using logarithmic distribution."""
        min_pop = 500_000
        max_pop = 500_000_000
        
        # Logarithmic distribution
        self.total_population = int(math.exp(random.uniform(math.log(min_pop), math.log(max_pop))))
        
        # Generate age distribution
        self._generate_age_distribution()
        
        # Generate wealth distribution
        self._generate_wealth_distribution()
        
        # Generate education
        self.education_technical = random.uniform(20, 80)
        self.education_cultural = random.uniform(20, 80)
    
    def _generate_age_distribution(self, gdp: float = 1e9, stability: float = 50, technology: float = 50):
        """Generate age groups based on demographic factors."""
        # Calculate age factor based on GDP, stability, and technology
        max_gdp = 1e12  # Reference maximum GDP
        age_factor = random.uniform(0, 1) * (gdp / max_gdp) * (stability / 100) * (technology / 100)
        
        # Base distribution percentages
        base_children = 0.25
        base_young_adults = 0.35
        base_older_adults = 0.25
        base_elderly = 0.15
        
        # Adjust based on age factor
        # Higher age_factor = more elderly, fewer children
        children_pct = base_children - (age_factor * 0.1)
        young_adults_pct = base_young_adults - (age_factor * 0.05)
        older_adults_pct = base_older_adults
        elderly_pct = base_elderly + (age_factor * 0.15)
        
        # Normalize to ensure sum = 1
        total = children_pct + young_adults_pct + older_adults_pct + elderly_pct
        children_pct /= total
        young_adults_pct /= total
        older_adults_pct /= total
        elderly_pct /= total
        
        # Create age groups
        self.age_groups = {
            "children": AgeGroup("Children", 0, 17, int(self.total_population * children_pct)),
            "young_adults": AgeGroup("Young Adults", 18, 39, int(self.total_population * young_adults_pct)),
            "older_adults": AgeGroup("Older Adults", 40, 65, int(self.total_population * older_adults_pct)),
            "elderly": AgeGroup("Elderly", 66, 90, int(self.total_population * elderly_pct))
        }
    
    def _generate_wealth_distribution(self):
        """Generate economic classes based on disparity factor."""
        # Random disparity factor (0.0 = equal, 1.0 = highly unequal)
        self.disparity_factor = random.uniform(0.1, 0.9)
        
        # Base distribution (more equal)
        lower_pop = 0.40
        middle_pop = 0.45
        upper_pop = 0.12
        elite_pop = 0.03
        
        # Adjust based on disparity
        # Higher disparity = more extreme distribution
        lower_pop += self.disparity_factor * 0.1
        middle_pop -= self.disparity_factor * 0.15
        upper_pop += self.disparity_factor * 0.03
        elite_pop += self.disparity_factor * 0.02
        
        # Normalize
        total = lower_pop + middle_pop + upper_pop + elite_pop
        lower_pop /= total
        middle_pop /= total
        upper_pop /= total
        elite_pop /= total
        
        # Wealth distribution (more unequal than population)
        lower_wealth = 0.10 - (self.disparity_factor * 0.05)
        middle_wealth = 0.40 - (self.disparity_factor * 0.15)
        upper_wealth = 0.35 + (self.disparity_factor * 0.10)
        elite_wealth = 0.15 + (self.disparity_factor * 0.10)
        
        # Normalize
        total = lower_wealth + middle_wealth + upper_wealth + elite_wealth
        lower_wealth /= total
        middle_wealth /= total
        upper_wealth /= total
        elite_wealth /= total
        
        self.economic_classes = {
            "lower": EconomicClass("Lower Class", lower_pop, lower_wealth),
            "middle": EconomicClass("Middle Class", middle_pop, middle_wealth),
            "upper": EconomicClass("Upper Class", upper_pop, upper_wealth),
            "elite": EconomicClass("Elite Class", elite_pop, elite_wealth)
        }
    
    def simulate_year(self, gdp: float, stability: float, technology: float):
        """Simulate population changes for one year."""
        # Recalculate age distribution based on current factors
        self._generate_age_distribution(gdp, stability, technology)
        
        # Population growth rate based on stability, technology, and age distribution
        growth_rate = (stability / 100 - 0.5) * 0.02 + (technology / 100 - 0.5) * 0.01
        
        # Younger population grows faster
        youth_ratio = self.age_groups["children"].population / self.total_population
        growth_rate += (youth_ratio - 0.25) * 0.02
        
        # Apply growth
        self.total_population = int(self.total_population * (1 + growth_rate))
        
        # Update age group populations
        for group in self.age_groups.values():
            group.population = int(group.population * (1 + growth_rate))
    
    def update_education(self, gdp: float, technology: float):
        """Slowly evolve education levels."""
        # Education improves with GDP and technology
        improvement = (gdp / 1e12) * 0.1 + (technology / 100) * 0.05
        
        self.education_technical = min(100, self.education_technical + improvement * random.uniform(0, 1))
        self.education_cultural = min(100, self.education_cultural + improvement * random.uniform(0, 1))
