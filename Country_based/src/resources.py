"""
Natural resources system - handles minerals, fossil fuels, and other resources.
"""

import random
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Mineral:
    """Represents a mineral resource."""
    name: str
    reserves: float
    extraction_capacity: float


@dataclass
class OilField:
    """Represents an oil field."""
    total_amount: float
    extraction_difficulty: float
    oil_quality: float
    current_extraction: float = 0.0


@dataclass
class GasReserve:
    """Represents a natural gas reserve."""
    total_amount: float
    extraction_difficulty: float
    current_extraction: float = 0.0


@dataclass
class Forest:
    """Represents a forest area."""
    area: float
    density: float
    wood_reserves: float


class NaturalResources:
    """Manages natural resources for a country."""
    
    def __init__(self, area: float, geography):
        self.area = area
        self.geography = geography
        
        # Minerals
        self.minerals: Dict[str, Mineral] = self._generate_minerals()
        
        # Fossil fuels
        self.oil_fields: List[OilField] = self._generate_oil_fields()
        self.gas_reserves: List[GasReserve] = self._generate_gas_reserves()
        
        # Forests
        self.forests: List[Forest] = self._generate_forests()
    
    def _generate_minerals(self) -> Dict[str, Mineral]:
        """Generate mineral reserves based on area."""
        minerals = {}
        mineral_types = ["Stone", "Iron", "Lithium", "Silicon"]
        base_area = 100000  # Reference area for normalization
        
        for mineral in mineral_types:
            min_reserve = 5000
            max_reserve = 1000000
            reserves = random.uniform(min_reserve, max_reserve) * (self.area / base_area)
            extraction_capacity = reserves * random.uniform(0.01, 0.05)
            
            minerals[mineral] = Mineral(
                name=mineral,
                reserves=reserves,
                extraction_capacity=extraction_capacity
            )
        
        return minerals
    
    def _generate_oil_fields(self) -> List[OilField]:
        """Generate oil fields."""
        num_fields = random.randint(0, 5)
        fields = []
        
        for _ in range(num_fields):
            total_amount = random.uniform(0, 100) * 1e9  # 0-100 billion barrels
            extraction_difficulty = random.uniform(0.1, 1.0)
            oil_quality = random.uniform(0.5, 1.0)
            
            fields.append(OilField(
                total_amount=total_amount,
                extraction_difficulty=extraction_difficulty,
                oil_quality=oil_quality
            ))
        
        return fields
    
    def _generate_gas_reserves(self) -> List[GasReserve]:
        """Generate natural gas reserves."""
        num_reserves = random.randint(0, 4)
        reserves = []
        
        for _ in range(num_reserves):
            total_amount = random.uniform(0, 50) * 1e12  # 0-50 trillion cubic meters
            extraction_difficulty = random.uniform(0.1, 1.0)
            
            reserves.append(GasReserve(
                total_amount=total_amount,
                extraction_difficulty=extraction_difficulty
            ))
        
        return reserves
    
    def _generate_forests(self) -> List[Forest]:
        """Generate forest areas based on geography."""
        num_forests = random.randint(1, 4)
        forests = []
        
        total_forest_area = self.area * random.uniform(0.1, 0.5)
        
        for _ in range(num_forests):
            area = total_forest_area / num_forests * random.uniform(0.5, 1.5)
            density = random.uniform(0.3, 0.9)
            wood_reserves = area * density * 1000  # Arbitrary units
            
            forests.append(Forest(
                area=area,
                density=density,
                wood_reserves=wood_reserves
            ))
        
        return forests
    
    def yearly_extract(self):
        """Extract resources for one year."""
        # Extract minerals
        for mineral in self.minerals.values():
            extracted = min(mineral.reserves, mineral.extraction_capacity)
            mineral.reserves -= extracted
            # Extraction capacity decreases as reserves deplete
            mineral.extraction_capacity = mineral.extraction_capacity * 0.99 + (mineral.reserves * 0.01)
        
        # Extract oil
        for field in self.oil_fields:
            if field.total_amount > 0:
                extraction_rate = 0.02 / field.extraction_difficulty
                extracted = min(field.total_amount, field.total_amount * extraction_rate)
                field.total_amount -= extracted
                field.current_extraction = extracted
        
        # Extract gas
        for reserve in self.gas_reserves:
            if reserve.total_amount > 0:
                extraction_rate = 0.03 / reserve.extraction_difficulty
                extracted = min(reserve.total_amount, reserve.total_amount * extraction_rate)
                reserve.total_amount -= extracted
                reserve.current_extraction = extracted
        
        # Extract wood (renewable)
        for forest in self.forests:
            extraction = forest.wood_reserves * 0.01  # 1% annual extraction
            forest.wood_reserves -= extraction
            # Regrowth
            regrowth = forest.area * forest.density * 50  # Regrowth rate
            forest.wood_reserves = min(forest.area * forest.density * 1000, 
                                       forest.wood_reserves + regrowth)
    
    def get_total_resource_value(self) -> float:
        """Calculate total estimated value of all resources."""
        value = 0.0
        
        # Mineral value
        for mineral in self.minerals.values():
            value += mineral.reserves * 100  # Arbitrary valuation
        
        # Oil value
        for field in self.oil_fields:
            value += field.total_amount * field.oil_quality * 50
        
        # Gas value
        for reserve in self.gas_reserves:
            value += reserve.total_amount * 10
        
        # Wood value
        for forest in self.forests:
            value += forest.wood_reserves * 5
        
        return value
