"""
Industries system - handles industry distribution, productivity, and output.
"""
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resources import NaturalResources
    from geography import Geography
    from population import Population


@dataclass
class IndustryOutput:
    """Represents the output and profit of an industry."""
    output: float
    profit: float
    workers: int


class Industries:
    """Manages industry distribution and output calculation."""
    
    def __init__(self):
        self.resource_share: float = 0.0
        self.agriculture_share: float = 0.0
        self.manufacturing_share: float = 0.0
        self.technology_share: float = 0.0
        
        self.resource_output: IndustryOutput = IndustryOutput(0, 0, 0)
        self.agriculture_output: IndustryOutput = IndustryOutput(0, 0, 0)
        self.manufacturing_output: IndustryOutput = IndustryOutput(0, 0, 0)
        self.technology_output: IndustryOutput = IndustryOutput(0, 0, 0)
        
        # Market prices (arbitrary units)
        self.resource_market_price = 100.0
        self.food_price = 50.0
        self.manufactured_goods_price = 150.0
        self.technology_price = 200.0
        self.worker_cost = 50000.0  # Annual cost per worker
        self.difficulty_cost = 1000000.0  # Cost multiplier for extraction difficulty
        
        # Shortage penalties
        self.food_ratio: float = 1.0
        self.resource_ratio: float = 1.0
        self.agriculture_penalty: float = 0.0
        self.resource_penalty: float = 0.0
        self.effective_productivity: float = 1.0
    
    def calculate_industry_shares(self, resources: 'NaturalResources', geography: 'Geography',
                                  population: 'Population', technology_level: float, gdp_per_capita: float):
        """Calculate industry distribution based on country characteristics."""
        # Calculate weights
        resource_weight = (
            resources.get_mineral_abundance()
            + resources.get_oil_abundance()
            + resources.get_gas_abundance()
            + resources.get_forest_abundance()
        )
        
        agriculture_weight = (
            geography.get_farmable_land_percent()
            * geography.get_fresh_water_factor()
        )
        
        infrastructure = 50.0  # Placeholder, would come from actual infrastructure
        manufacturing_weight = (
            technology_level
            + population.technical_education
            + infrastructure
        )
        
        gdp_per_capita_factor = min(1.0, gdp_per_capita / 50000)
        technology_weight = (
            technology_level * 2
            + population.technical_education
            + gdp_per_capita_factor * 100
        )
        
        # Normalize to get shares
        total_weight = resource_weight + agriculture_weight + manufacturing_weight + technology_weight
        if total_weight > 0:
            self.resource_share = resource_weight / total_weight
            self.agriculture_share = agriculture_weight / total_weight
            self.manufacturing_share = manufacturing_weight / total_weight
            self.technology_share = technology_weight / total_weight
        else:
            # Equal distribution if all weights are zero
            self.resource_share = 0.25
            self.agriculture_share = 0.25
            self.manufacturing_share = 0.25
            self.technology_share = 0.25
    
    def calculate_productivity(self, technology_level: float, technical_education: float,
                             infrastructure: float, stability: float, cultural_education: float) -> float:
        """Calculate common productivity multiplier."""
        productivity = (
            0.30 * technology_level
            + 0.25 * technical_education
            + 0.20 * infrastructure
            + 0.15 * stability
            + 0.10 * cultural_education
        ) / 100
        return max(0.1, min(2.0, productivity))
    
    def calculate_outputs(self, resources: 'NaturalResources', geography: 'Geography',
                          population: 'Population', technology_level: float, 
                          technical_education: float, infrastructure: float, 
                          stability: float, cultural_education: float,
                          unemployment_rate: float):
        """Calculate industry outputs and profits."""
        # Calculate productivity
        base_productivity = self.calculate_productivity(
            technology_level, technical_education, infrastructure, stability, cultural_education
        )
        
        # Apply shortage penalties
        self.effective_productivity = (
            base_productivity
            * (1 - 0.4 * self.agriculture_penalty)
            * (1 - 0.4 * self.resource_penalty)
        )
        
        # Calculate working population
        working_age_population = population.get_working_age_population()
        working_population = int(working_age_population * (1 - unemployment_rate / 100))
        
        # Distribute workers
        resource_workers = int(working_population * self.resource_share)
        agriculture_workers = int(working_population * self.agriculture_share)
        manufacturing_workers = int(working_population * self.manufacturing_share)
        technology_workers = int(working_population * self.technology_share)
        
        # Resource extraction output
        extracted_resources = (
            sum(m.yearly_extraction_capacity for m in resources.minerals.values())
            + resources.get_total_oil() * 0.02
            + resources.get_total_gas() * 0.03
        )
        
        avg_difficulty = 0.5
        if resources.oil_fields:
            avg_difficulty = sum(f.extraction_difficulty for f in resources.oil_fields) / len(resources.oil_fields)
        
        resource_output_value = extracted_resources * self.resource_market_price
        resource_cost = resource_workers * self.worker_cost + avg_difficulty * self.difficulty_cost
        self.resource_output = IndustryOutput(resource_output_value, resource_output_value - resource_cost, resource_workers)
        
        # Agriculture output
        farmable_land_factor = geography.get_farmable_land_percent() / 100
        fresh_water_factor = geography.get_fresh_water_factor()
        
        agriculture_output_value = (
            agriculture_workers
            * self.effective_productivity
            * farmable_land_factor
            * fresh_water_factor
            * 1000  # Scaling factor
        )
        agriculture_cost = agriculture_workers * self.worker_cost
        self.agriculture_output = IndustryOutput(
            agriculture_output_value,
            agriculture_output_value * self.food_price - agriculture_cost,
            agriculture_workers
        )
        
        # Manufacturing output
        manufacturing_output_value = (
            manufacturing_workers
            * self.effective_productivity
            * (1 + technology_level / 100)
            * 1000
        )
        manufacturing_cost = manufacturing_workers * self.worker_cost
        self.manufacturing_output = IndustryOutput(
            manufacturing_output_value,
            manufacturing_output_value * self.manufactured_goods_price - manufacturing_cost,
            manufacturing_workers
        )
        
        # Technology output
        technology_output_value = (
            technology_workers
            * self.effective_productivity
            * (1 + technology_level / 50)
            * (1 + technical_education / 100)
            * 1000
        )
        technology_cost = technology_workers * self.worker_cost
        self.technology_output = IndustryOutput(
            technology_output_value,
            technology_output_value * self.technology_price - technology_cost,
            technology_workers
        )
    
    def calculate_shortage_penalties(self, population: int, technology_level: float):
        """Calculate resource shortage penalties."""
        # Demand calculations
        food_per_capita = 1.0  # Arbitrary units
        resource_intensity = 0.5 + (technology_level / 100) * 0.5  # Higher tech needs more resources
        
        food_demand = population * food_per_capita
        resource_demand = population * resource_intensity
        
        food_supply = self.agriculture_output.output / self.food_price
        resource_supply = self.resource_output.output / self.resource_market_price
        
        # Calculate ratios
        self.food_ratio = min(1.0, food_supply / food_demand) if food_demand > 0 else 1.0
        self.resource_ratio = min(1.0, resource_supply / resource_demand) if resource_demand > 0 else 1.0
        
        # Nonlinear penalty
        def shortage_penalty(ratio: float) -> float:
            return max(0.0, (1.0 - ratio) ** 2)
        
        self.agriculture_penalty = shortage_penalty(self.food_ratio)
        self.resource_penalty = shortage_penalty(self.resource_ratio)
    
    def get_total_gdp(self) -> float:
        """Get total GDP from all industries."""
        return (
            self.resource_output.output
            + self.agriculture_output.output
            + self.manufacturing_output.output
            + self.technology_output.output
        )
    
    def get_total_profit(self) -> float:
        """Get total corporate profit from all industries."""
        return (
            self.resource_output.profit
            + self.agriculture_output.profit
            + self.manufacturing_output.profit
            + self.technology_output.profit
        )
