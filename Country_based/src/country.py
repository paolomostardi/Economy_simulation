"""
Country class - Main class representing a country in the simulation.
"""
import random
import math
from typing import Dict, List
from geography import Geography
from culture import Culture, EducationSystemType
from resources import NaturalResources
from population import Population
from industries import Industries
from economy import Economy, BudgetAllocation


class Country:
    """Represents a country in the economy simulation."""
    
    def __init__(self, name: str, country_id: int):
        self.id = country_id
        self.name = name
        
        # Basic properties
        self.area: float = 0.0
        self.stability: float = 0.0
        self.technology: float = 0.0
        self.corruption: float = 0.0
        self.democracy_index: float = 0.0
        
        # Subsystems
        self.geography: Geography = None
        self.culture: Culture = None
        self.resources: NaturalResources = None
        self.population: Population = None
        self.industries: Industries = None
        self.economy: Economy = None
        
        # Initialize all systems
        self._initialize_properties()
    
    def _initialize_properties(self):
        """Initialize all country properties based on requirements."""
        # Generate population first (affects area and other properties)
        self.population = Population()
        self.population.generate_population()
        
        # Generate area based on population
        self._generate_area()
        
        # Generate geography (needs area)
        self.geography = Geography(self.area, 0)  # Forest area will be updated after resources
        
        # Generate resources (needs area)
        self.resources = NaturalResources(self.area)
        
        # Update geography with actual forest area
        self.geography = Geography(self.area, self.resources.get_total_forest_area())
        
        # Generate culture
        self.culture = Culture()
        
        # Generate basic properties
        self.stability = random.uniform(30, 90)
        self.technology = random.uniform(20, 95)
        self.democracy_index = random.uniform(20, 80)
        self.corruption = self._generate_corruption()
        
        # Generate industries
        self.industries = Industries()
        
        # Generate economy
        self.economy = Economy(
            self.population.total_population,
            self.stability,
            self.technology,
            self.corruption,
            self.democracy_index,
            self.population.age_groups
        )
        
        # Initial industry calculation
        self._calculate_industries()
    
    def _generate_area(self):
        """Generate land area based on population."""
        pop = self.population.total_population
        min_area = 1000 + (pop / 500000000) * 50000
        max_area = 10000 + (pop / 500000000) * 900000
        
        self.area = math.exp(random.uniform(math.log(min_area), math.log(max_area)))
    
    def _generate_corruption(self) -> float:
        """Generate corruption level using the specified formula."""
        if random.uniform(0, 1) < 0.4:
            return random.uniform(15, 30)
        else:
            if random.uniform(0, 1) < 0.4:
                return 15 * math.exp(-random.uniform(0, 3))
            else:
                return 30 + 70 * (1 - math.exp(-random.uniform(0, 3)))
    
    def _calculate_industries(self):
        """Calculate industry distribution and outputs."""
        self.industries.calculate_industry_shares(
            self.resources,
            self.geography,
            self.population,
            self.technology,
            self.economy.gdp_per_capita
        )
        
        infrastructure = 50.0  # Placeholder
        self.industries.calculate_outputs(
            self.resources,
            self.geography,
            self.population,
            self.technology,
            self.population.technical_education,
            infrastructure,
            self.stability,
            self.population.cultural_education,
            self.economy.unemployment_rate
        )
        
        self.industries.calculate_shortage_penalties(
            self.population.total_population,
            self.technology
        )
        
        # Update economy from industries
        self.economy.update_from_industries(self.industries)
    
    def simulate_year(self, year: int):
        """Simulate one year for this country."""
        # Calculate industries first (GDP depends on this)
        self._calculate_industries()
        
        # Apply shortage penalties to stability (much less severe)
        shortage_penalty = (
            5 * self.industries.agriculture_penalty
            + 3 * self.industries.resource_penalty
        )
        
        # Add positive factors for stability
        education_bonus = self.population.cultural_education / 100 * 3
        healthcare_bonus = (self.economy.healthcare_spending / 1e9) * 5
        infrastructure_bonus = (self.economy.infrastructure_spending / 1e9) * 3
        gdp_growth_bonus = max(0, self.economy.gdp_growth_rate) * 10
        
        corruption_penalty = self.corruption / 100 * 3
        unemployment_penalty = self.economy.unemployment_rate / 40 * 3
        inequality_penalty = self.population.disparity_factor * 3
        
        stability_change = (
            education_bonus + healthcare_bonus + infrastructure_bonus + gdp_growth_bonus
        ) - (
            shortage_penalty + corruption_penalty + unemployment_penalty + inequality_penalty
        )
        
        # Apply change with natural recovery tendency
        self.stability += stability_change
        # Natural tendency toward moderate stability (stronger recovery)
        if self.stability < 50:
            self.stability += 2.0
        elif self.stability > 80:
            self.stability -= 1.0
        
        self.stability = max(0, min(100, self.stability))
        
        # Update population
        max_gdp_per_capita = 50000.0
        self.population.simulate_year(
            self.economy.gdp_per_capita,
            max_gdp_per_capita,
            self.stability,
            self.corruption,
            self.economy.unemployment_rate,
            self.democracy_index,
            self.economy.healthcare_spending,
            self.technology,
            self.geography.get_fresh_water_factor()
        )
        
        # Update education
        self.population.update_education(
            self.economy.education_spending,
            self.technology
        )
        
        # Update economy
        infrastructure = 50.0 + (self.economy.infrastructure_spending / 1e9) * 10
        self.economy.yearly_update(
            self.population.total_population,
            self.stability,
            self.technology,
            self.corruption,
            self.democracy_index,
            self.population.age_groups,
            self.industries.agriculture_penalty,
            self.industries.resource_penalty
        )
        
        # Update democracy
        democracy_change = (
            self.population.cultural_education / 100
            + (self.democracy_index / 100) * 0.01  # Transparency bonus
        ) - (
            self.corruption / 100
            + (1 - self.stability / 100) * 0.05  # Instability penalty
        )
        self.democracy_index = max(0, min(100, self.democracy_index + democracy_change))
        
        # Update corruption (affected by democracy)
        corruption_modifier = 1 - self.democracy_index / 200
        target_corruption = self.corruption * corruption_modifier
        self.corruption = max(0, min(100, self.corruption * 0.95 + target_corruption * 0.05))
        
        # Technology slowly improves
        tech_improvement = (self.economy.research_spending / 1e9) * 2 + random.uniform(0, 0.5)
        self.technology = max(0, min(100, self.technology + tech_improvement))
        
        # Extract resources
        self.resources.simulate_year()
    
    def get_summary(self) -> str:
        """Get a summary of the country's state."""
        return (
            f"{self.name}: "
            f"Pop={self.population.total_population:,}, "
            f"GDP=${self.economy.gdp/1e9:,.2f}B, "
            f"Stability={self.stability:.1f}, "
            f"Tech={self.technology:.1f}, "
            f"Corruption={self.corruption:.1f}%"
        )
    
    def to_dict(self) -> Dict:
        """Convert country data to dictionary for output."""
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population.total_population,
            "gdp": self.economy.gdp,
            "gdp_per_capita": self.economy.gdp_per_capita,
            "stability": self.stability,
            "democracy": self.democracy_index,
            "corruption": self.corruption,
            "unemployment": self.economy.unemployment_rate,
            "net_migration": self.population.net_migration,
            "birth_rate": self.population.birth_rate,
            "death_rate": sum(g.mortality_rate for g in self.population.age_groups.values()) / 4,
            "inflation": self.economy.inflation,
            "technology": self.technology,
            "resource_reserve_index": self.resources.get_mineral_abundance()
        }
