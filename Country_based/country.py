"""
Country class - Main class representing a country in the simulation.
"""
import random
import math
from typing import Dict, List
from population import PopulationManager
from resources import ResourceManager
from economy import EconomyManager
from culture import CultureManager


class Country:
    """Represents a country in the economy simulation."""
    
    def __init__(self, name: str):
        self.name = name
        
        # Basic properties
        self.population_manager = PopulationManager()
        self.resource_manager = ResourceManager()
        self.economy_manager = EconomyManager()
        self.culture_manager = CultureManager()
        
        # Initialize all systems
        self._initialize_properties()
    
    def _initialize_properties(self):
        """Initialize all country properties based on requirements."""
        # Generate population first (affects area and other properties)
        self.population_manager.generate_population()
        
        # Generate area based on population
        self._generate_area()
        
        # Generate resources based on area
        self.resource_manager.generate_resources(self.area)
        
        # Generate culture
        self.culture_manager.generate_culture()
        
        # Generate economy based on resources, population, and culture
        self.economy_manager.generate_economy(
            self.population_manager.total_population,
            self.resource_manager,
            self.population_manager.education_technical,
            self.population_manager.education_cultural
        )
        
        # Generate stability and technology
        self.stability = random.uniform(30, 90)
        self.technology = random.uniform(20, 95)
        
        # Generate corruption
        self.corruption = self._generate_corruption()
    
    def _generate_area(self):
        """Generate land area based on population."""
        # Area is related to population - larger population tends to have larger area
        # Base area range influenced by population size
        pop = self.population_manager.total_population
        min_area = 1000 + (pop / 500000000) * 50000  # 1,000 to 51,000 km² minimum
        max_area = 10000 + (pop / 500000000) * 900000  # 10,000 to 910,000 km² maximum
        
        # Use logarithmic distribution for area
        self.area = math.exp(random.uniform(math.log(min_area), math.log(max_area)))
    
    def _generate_corruption(self) -> float:
        """Generate corruption level using the specified formula."""
        if random.uniform(0, 1) < 0.4:
            # Uniform distribution between 15 and 30 (40% probability)
            return random.uniform(15, 30)
        else:
            # Not in normal range (60% probability)
            if random.uniform(0, 1) < 0.4:
                # Logarithmic distribution from 15 down to 0 (24% probability)
                return 15 * math.exp(-random.uniform(0, 3))
            else:
                # Logarithmic distribution from 30 up to 100 (36% probability)
                return 30 + 70 * (1 - math.exp(-random.uniform(0, 3)))
    
    @property
    def population(self) -> int:
        """Total population."""
        return self.population_manager.total_population
    
    @property
    def gdp(self) -> float:
        """Total GDP."""
        return self.economy_manager.gdp
    
    @property
    def tax_rate(self) -> float:
        """Tax rate percentage."""
        return self.economy_manager.tax_rate
    
    @property
    def government_revenue(self) -> float:
        """Government revenue before corruption."""
        return self.economy_manager.government_revenue
    
    @property
    def effective_revenue(self) -> float:
        """Government revenue after corruption."""
        return self.economy_manager.effective_revenue
    
    def simulate_year(self, year: int):
        """Simulate one year for this country."""
        # Update population
        self.population_manager.simulate_year(
            self.economy_manager.gdp,
            self.stability,
            self.technology
        )
        
        # Extract resources
        self.resource_manager.simulate_year()
        
        # Update economy
        self.economy_manager.simulate_year(
            self.population_manager.total_population,
            self.resource_manager,
            self.stability,
            self.technology,
            self.corruption
        )
        
        # Update education slowly
        self.population_manager.update_education(self.economy_manager.gdp, self.technology)
        
        # Update stability (affected by inequality)
        inequality_impact = self.population_manager.disparity_factor * 0.5
        self.stability = max(0, min(100, self.stability - inequality_impact + random.uniform(-2, 2)))
        
        # Technology slowly improves
        self.technology = max(0, min(100, self.technology + random.uniform(0, 0.5)))
    
    def get_summary(self) -> str:
        """Get a summary of the country's state."""
        return (
            f"{self.name}: "
            f"Pop={self.population:,}, "
            f"GDP=${self.gdp:,.2f}B, "
            f"Stability={self.stability:.1f}, "
            f"Tech={self.technology:.1f}, "
            f"Corruption={self.corruption:.1f}%"
        )
