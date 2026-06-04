"""
Population system - handles population, age groups, birth/death rates, and migration.
"""
import random
import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class AgeGroup:
    """Represents an age group in the population."""
    name: str
    min_age: int
    max_age: int
    population: int
    mortality_rate: float


@dataclass
class EconomicClass:
    """Represents an economic class in the population."""
    name: str
    population_percentage: float
    wealth_percentage: float


class Population:
    """Manages population-related properties and calculations."""
    
    def __init__(self):
        self.total_population: int = 0
        self.age_groups: Dict[str, AgeGroup] = {}
        self.economic_classes: Dict[str, EconomicClass] = {}
        self.disparity_factor: float = 0.0  # 0.0 to 1.0, inequality level
        self.technical_education: float = 0.0  # 0 to 100
        self.cultural_education: float = 0.0  # 0 to 100
        
        # Rates
        self.birth_rate: float = 0.0
        self.immigration_rate: float = 0.0
        self.emigration_rate: float = 0.0
        self.net_migration: int = 0
        
        # Constants
        self.max_birth_rate = 0.05  # 5%
        self.max_immigration_rate = 0.03  # 3%
        self.max_emigration_rate = 0.03  # 3%
    
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
        self.technical_education = random.uniform(20, 80)
        self.cultural_education = random.uniform(20, 80)
    
    def _generate_age_distribution(self, gdp: float = 1e9, stability: float = 50, technology: float = 50):
        """Generate age groups based on demographic factors."""
        # Calculate age factor
        max_gdp = 1e12
        age_factor = random.uniform(0, 1) * (gdp / max_gdp) * (stability / 100) * (technology / 100)
        
        # Base distribution percentages
        base_children = 0.25
        base_young_adults = 0.35
        base_older_adults = 0.25
        base_elderly = 0.15
        
        # Adjust based on age factor
        children_pct = base_children - (age_factor * 0.1)
        young_adults_pct = base_young_adults - (age_factor * 0.05)
        older_adults_pct = base_older_adults
        elderly_pct = base_elderly + (age_factor * 0.15)
        
        # Normalize
        total = children_pct + young_adults_pct + older_adults_pct + elderly_pct
        children_pct /= total
        young_adults_pct /= total
        older_adults_pct /= total
        elderly_pct /= total
        
        # Create age groups with mortality rates
        self.age_groups = {
            "children": AgeGroup("Children", 0, 17, int(self.total_population * children_pct), 
                                random.uniform(0.0005, 0.005)),
            "young_adults": AgeGroup("Young Adults", 18, 39, int(self.total_population * young_adults_pct),
                                    random.uniform(0.0005, 0.003)),
            "older_adults": AgeGroup("Older Adults", 40, 65, int(self.total_population * older_adults_pct),
                                    random.uniform(0.002, 0.015)),
            "elderly": AgeGroup("Elderly", 66, 90, int(self.total_population * elderly_pct),
                               random.uniform(0.02, 0.12))
        }
    
    def _generate_wealth_distribution(self):
        """Generate economic classes based on disparity factor."""
        self.disparity_factor = random.uniform(0.1, 0.9)
        
        # Base distribution
        lower_pop = 0.40
        middle_pop = 0.45
        upper_pop = 0.12
        elite_pop = 0.03
        
        # Adjust based on disparity
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
        
        # Wealth distribution
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
    
    def calculate_rates(self, gdp_per_capita: float, max_gdp_per_capita: float, stability: float,
                       corruption: float, unemployment_rate: float, democracy_index: float):
        """Calculate birth, immigration, and emigration rates."""
        # Birth rate
        self.birth_rate = (
            random.uniform(0.4, 1.0)
            * (1 - gdp_per_capita / max_gdp_per_capita)
            * (stability / 100)
            * self.max_birth_rate
        )
        
        # Immigration rate
        self.immigration_rate = (
            random.uniform(0, 1)
            * (gdp_per_capita / max_gdp_per_capita)
            * (stability / 100)
            * (1 - corruption / 100)
            * self.max_immigration_rate
        )
        self.immigration_rate *= (1 - unemployment_rate / 100)
        
        # Emigration rate
        self.emigration_rate = (
            random.uniform(0, 1)
            * (1 - gdp_per_capita / max_gdp_per_capita)
            * (1 - stability / 100)
            * (corruption / 100)
            * self.max_emigration_rate
        )
        self.emigration_rate *= (1 + unemployment_rate / 50)
        
        # Democracy effect on emigration
        self.emigration_rate += (100 - democracy_index) * 0.0001
    
    def update_mortality_rates(self, healthcare_spending: float, technology: float, 
                               stability: float, fresh_water_factor: float):
        """Update mortality rates based on factors."""
        # Higher healthcare and technology reduce mortality
        # Lower stability increases mortality
        # Fresh water availability affects mortality
        
        for group in self.age_groups.values():
            base_mortality = group.mortality_rate
            
            # Apply modifiers
            healthcare_factor = 1.0 - (healthcare_spending / 1e9) * 0.3
            tech_factor = 1.0 - (technology / 100) * 0.2
            stability_factor = 1.0 + (1 - stability / 100) * 0.5
            water_factor = 1.0 - (1 - fresh_water_factor) * 0.3
            
            group.mortality_rate = base_mortality * healthcare_factor * tech_factor * stability_factor * water_factor
            group.mortality_rate = max(0.0001, min(0.2, group.mortality_rate))
    
    def simulate_year(self, gdp_per_capita: float, max_gdp_per_capita: float, stability: float,
                     corruption: float, unemployment_rate: float, democracy_index: float,
                     healthcare_spending: float, technology: float, fresh_water_factor: float):
        """Simulate population changes for one year."""
        # Calculate rates
        self.calculate_rates(gdp_per_capita, max_gdp_per_capita, stability, corruption,
                            unemployment_rate, democracy_index)
        
        # Update mortality rates
        self.update_mortality_rates(healthcare_spending, technology, stability, fresh_water_factor)
        
        # Calculate births
        births = int(self.total_population * self.birth_rate)
        
        # Calculate deaths
        deaths = 0
        for group in self.age_groups.values():
            deaths += int(group.population * group.mortality_rate)
        
        # Calculate migration
        immigration = int(self.total_population * self.immigration_rate)
        emigration = int(self.total_population * self.emigration_rate)
        self.net_migration = immigration - emigration
        
        # Update population
        self.total_population = max(0, self.total_population + births - deaths + self.net_migration)
        
        # Update age distribution
        self._generate_age_distribution(gdp_per_capita * self.total_population, stability, technology)
    
    def get_working_age_population(self) -> int:
        """Get working age population (young adults + older adults)."""
        return self.age_groups["young_adults"].population + self.age_groups["older_adults"].population
    
    def update_education(self, education_spending: float, technology: float):
        """Update education scores based on spending and technology."""
        improvement = (education_spending / 1e9) * 5 + (technology / 100) * 0.5
        self.technical_education = min(100, self.technical_education + improvement * random.uniform(0, 1))
        self.cultural_education = min(100, self.cultural_education + improvement * random.uniform(0, 1))
