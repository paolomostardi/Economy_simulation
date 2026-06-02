"""
Population system - handles demographics, age distribution, and population dynamics.
"""

import random
import math
from typing import Dict
from dataclasses import dataclass


@dataclass
class AgeGroup:
    """Represents an age group in the population."""
    children: int = 0      # 0-17 years
    young_adults: int = 0  # 18-39 years
    older_adults: int = 0  # 40-65 years
    elderly: int = 0       # 66-90 years


@dataclass
class EconomicClass:
    """Represents economic class distribution."""
    lower_class: int = 0
    middle_class: int = 0
    upper_class: int = 0
    elite_class: int = 0


class Population:
    """Manages population demographics and dynamics."""
    
    def __init__(self, area: float, stability: float, technology: float):
        self.total = self._generate_population()
        
        # Wealth distribution (initialize before economic classes)
        self.inequality_factor = random.uniform(0.2, 0.8)
        
        self.age_groups = self._generate_age_distribution(stability, technology)
        self.economic_classes = self._generate_economic_classes()
        
        # Population dynamics
        self.birth_rate = 0.0
        self.immigration_rate = 0.0
        self.emigration_rate = 0.0
        
        # Mortality rates (yearly percentages)
        self.mortality_rates = {
            "children": random.uniform(0.0005, 0.0050),
            "young_adults": random.uniform(0.0005, 0.0030),
            "older_adults": random.uniform(0.0020, 0.0150),
            "elderly": random.uniform(0.0200, 0.1200)
        }
    
    def _generate_population(self) -> int:
        """Generate population using logarithmic distribution."""
        min_pop = 500000
        max_pop = 500000000
        population = math.exp(random.uniform(math.log(min_pop), math.log(max_pop)))
        return int(population)
    
    def _generate_age_distribution(self, stability: float, technology: float) -> AgeGroup:
        """Generate age distribution based on demographic factors."""
        # Base distribution (realistic demographics)
        base_children = 0.25
        base_young = 0.30
        base_older = 0.30
        base_elderly = 0.15
        
        # Age factor based on GDP proxy (using stability and technology)
        age_factor = random.uniform(0, 1) * (stability / 100) * (technology / 100)
        
        # Adjust distribution based on age_factor
        if age_factor > 0.5:
            # Older population
            base_children -= 0.05
            base_young -= 0.05
            base_older += 0.05
            base_elderly += 0.05
        else:
            # Younger population
            base_children += 0.05
            base_young += 0.05
            base_older -= 0.05
            base_elderly -= 0.05
        
        # Ensure valid distribution
        total = base_children + base_young + base_older + base_elderly
        base_children /= total
        base_young /= total
        base_older /= total
        base_elderly /= total
        
        return AgeGroup(
            children=int(self.total * base_children),
            young_adults=int(self.total * base_young),
            older_adults=int(self.total * base_older),
            elderly=int(self.total * base_elderly)
        )
    
    def _generate_economic_classes(self) -> EconomicClass:
        """Generate economic class distribution based on inequality factor."""
        # Base distribution for moderate inequality
        base_lower = 0.40
        base_middle = 0.45
        base_upper = 0.12
        base_elite = 0.03
        
        # Adjust based on inequality factor
        if self.inequality_factor > 0.6:
            # High inequality
            base_lower += 0.10
            base_middle -= 0.10
            base_upper += 0.02
            base_elite -= 0.02
        elif self.inequality_factor < 0.4:
            # Low inequality
            base_lower -= 0.10
            base_middle += 0.10
            base_upper -= 0.02
            base_elite += 0.02
        
        # Ensure valid distribution
        total = base_lower + base_middle + base_upper + base_elite
        base_lower /= total
        base_middle /= total
        base_upper /= total
        base_elite /= total
        
        return EconomicClass(
            lower_class=int(self.total * base_lower),
            middle_class=int(self.total * base_middle),
            upper_class=int(self.total * base_upper),
            elite_class=int(self.total * base_elite)
        )
    
    def yearly_update(self, gdp_per_capita: float, stability: float, corruption: float,
                     unemployment_rate: float, healthcare_spending: float, technology: float):
        """Update population for one year."""
        # Calculate rates
        self._calculate_rates(gdp_per_capita, stability, corruption, unemployment_rate)
        
        # Calculate population changes
        births = self.total * self.birth_rate
        deaths = self._calculate_deaths(healthcare_spending, technology, stability)
        immigration = self.total * self.immigration_rate
        emigration = self.total * self.emigration_rate
        
        # Apply changes
        population_change = (births - deaths) + (immigration - emigration)
        self.total = max(100000, int(self.total + population_change))
        
        # Update age distribution
        self._update_age_distribution(births, deaths, immigration, emigration)
        
        # Update economic classes
        self._update_economic_classes()
    
    def _calculate_rates(self, gdp_per_capita: float, stability: float, corruption: float,
                        unemployment_rate: float):
        """Calculate birth, immigration, and emigration rates."""
        max_gdp_per_capita = 100000  # Reference maximum
        max_birth_rate = 0.05
        max_immigration_rate = 0.03
        max_emigration_rate = 0.03
        
        # Birth rate
        self.birth_rate = (
            random.uniform(0.4, 1.0)
            * (1 - min(1, gdp_per_capita / max_gdp_per_capita))
            * (stability / 100)
            * max_birth_rate
        )
        
        # Immigration rate
        self.immigration_rate = (
            random.uniform(0, 1)
            * (min(1, gdp_per_capita / max_gdp_per_capita))
            * (stability / 100)
            * (1 - corruption / 100)
            * max_immigration_rate
        )
        self.immigration_rate *= (1 - unemployment_rate / 100)
        
        # Emigration rate
        self.emigration_rate = (
            random.uniform(0, 1)
            * (1 - min(1, gdp_per_capita / max_gdp_per_capita))
            * (1 - stability / 100)
            * (corruption / 100)
            * max_emigration_rate
        )
        self.emigration_rate *= (1 + unemployment_rate / 50)
    
    def _calculate_deaths(self, healthcare_spending: float, technology: float, stability: float) -> int:
        """Calculate total deaths based on mortality rates."""
        # Adjust mortality rates based on factors
        health_factor = 1 - (healthcare_spending / 1000000000000) * 0.3  # Reduced by healthcare
        tech_factor = 1 - (technology / 100) * 0.2  # Reduced by technology
        stability_factor = 1 + (1 - stability / 100) * 0.3  # Increased by low stability
        
        adjustment = health_factor * tech_factor * stability_factor
        
        deaths = (
            self.age_groups.children * self.mortality_rates["children"] * adjustment +
            self.age_groups.young_adults * self.mortality_rates["young_adults"] * adjustment +
            self.age_groups.older_adults * self.mortality_rates["older_adults"] * adjustment +
            self.age_groups.elderly * self.mortality_rates["elderly"] * adjustment
        )
        
        return int(deaths)
    
    def _update_age_distribution(self, births: float, deaths: float, 
                                 immigration: float, emigration: float):
        """Update age distribution with aging and migration."""
        # Age progression
        new_elderly = self.age_groups.older_adults
        new_older_adults = self.age_groups.young_adults
        new_young_adults = self.age_groups.children
        
        # New births become children
        new_children = int(births)
        
        # Apply deaths (disproportionately from elderly)
        elderly_deaths = int(deaths * 0.4)
        other_deaths = int(deaths * 0.6)
        
        new_elderly = max(0, new_elderly - elderly_deaths)
        new_older_adults = max(0, new_older_adults - int(other_deaths * 0.3))
        new_young_adults = max(0, new_young_adults - int(other_deaths * 0.2))
        new_children = max(0, new_children - int(other_deaths * 0.1))
        
        # Apply migration (immigrants/emigrants tend to be young adults)
        net_migration = int(immigration - emigration)
        new_young_adults += net_migration
        
        # Update age groups
        self.age_groups = AgeGroup(
            children=new_children,
            young_adults=new_young_adults,
            older_adults=new_older_adults,
            elderly=new_elderly
        )
        
        # Recalculate total to match
        actual_total = sum([self.age_groups.children, self.age_groups.young_adults,
                           self.age_groups.older_adults, self.age_groups.elderly])
        
        # Adjust to match total (distribute difference)
        if actual_total != self.total:
            diff = self.total - actual_total
            self.age_groups.young_adults += diff
    
    def _update_economic_classes(self):
        """Update economic class distribution based on new total."""
        # Maintain proportions
        total_classes = sum([self.economic_classes.lower_class, self.economic_classes.middle_class,
                            self.economic_classes.upper_class, self.economic_classes.elite_class])
        
        if total_classes > 0:
            factor = self.total / total_classes
            self.economic_classes.lower_class = int(self.economic_classes.lower_class * factor)
            self.economic_classes.middle_class = int(self.economic_classes.middle_class * factor)
            self.economic_classes.upper_class = int(self.economic_classes.upper_class * factor)
            self.economic_classes.elite_class = int(self.economic_classes.elite_class * factor)
