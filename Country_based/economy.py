"""
Economy management - Handles GDP, tax rates, inflation, and government revenue.
"""
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resources import ResourceManager


class EconomyManager:
    """Manages economic properties and calculations."""
    
    def __init__(self):
        self.gdp: float = 0.0  # in billions
        self.gdp_growth_rate: float = 0.0  # percentage
        self.inflation: float = 0.0  # percentage
        self.tax_rate: float = 0.0  # percentage
        self.government_revenue: float = 0.0
        self.effective_revenue: float = 0.0
    
    def generate_economy(self, population: int, resource_manager: 'ResourceManager', 
                        education_technical: float, education_cultural: float):
        """Generate initial economy based on various factors."""
        # Base GDP from population
        base_gdp_per_capita = random.uniform(5_000, 50_000)  # USD
        population_gdp = (population * base_gdp_per_capita) / 1e9  # Convert to billions
        
        # Resource contribution
        resource_value = self._calculate_resource_value(resource_manager)
        
        # Education contribution
        education_bonus = (education_technical + education_cultural) / 200 * 0.5
        
        # Combine factors
        self.gdp = population_gdp * (1 + resource_value + education_bonus)
        
        # Initial tax rate
        self.tax_rate = random.uniform(10, 50)
        
        # Calculate revenue
        self._calculate_revenue()
        
        # Initial growth rate and inflation
        self.gdp_growth_rate = random.uniform(-2, 5)
        self.inflation = random.uniform(0, 10)
    
    def _calculate_resource_value(self, resource_manager: 'ResourceManager') -> float:
        """Calculate economic value of resources."""
        # Mineral value
        mineral_value = sum(m.current_reserves for m in resource_manager.minerals.values()) / 1e6
        
        # Oil value
        oil_value = resource_manager.get_total_oil() * 0.1
        
        # Gas value
        gas_value = resource_manager.get_total_gas() * 0.05
        
        # Forest value
        forest_value = resource_manager.get_total_forest_area() / 1000
        
        return (mineral_value + oil_value + gas_value + forest_value) * 0.1
    
    def _calculate_revenue(self):
        """Calculate government revenue."""
        self.government_revenue = self.gdp * (self.tax_rate / 100)
        # Effective revenue will be calculated with corruption factor in Country class
    
    def simulate_year(self, population: int, resource_manager: 'ResourceManager', 
                     stability: float, technology: float, corruption: float):
        """Simulate economy for one year."""
        # Calculate resource value
        resource_value = self._calculate_resource_value(resource_manager)
        
        # Growth rate based on stability, technology, and resources
        stability_factor = (stability - 50) / 100
        tech_factor = technology / 100
        resource_factor = resource_value * 0.5
        
        target_growth = stability_factor * 3 + tech_factor * 2 + resource_factor
        self.gdp_growth_rate = target_growth + random.uniform(-1, 1)
        
        # Apply growth
        self.gdp = self.gdp * (1 + self.gdp_growth_rate / 100)
        
        # Inflation based on growth rate
        self.inflation = max(0, self.gdp_growth_rate * 0.5 + random.uniform(-1, 2))
        
        # Tax rate may change slightly
        self.tax_rate = max(10, min(50, self.tax_rate + random.uniform(-1, 1)))
        
        # Calculate revenue
        self._calculate_revenue()
        
        # Apply corruption
        self.effective_revenue = self.government_revenue * (1 - corruption / 100)
