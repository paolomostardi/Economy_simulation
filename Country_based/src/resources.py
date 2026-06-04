"""
Natural Resources system - handles mineral, fossil fuel, and forest resources.
"""
import random
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Mineral:
    """Represents a mineral resource."""
    name: str
    total_reserves: float
    yearly_extraction_capacity: float
    current_reserves: float


@dataclass
class OilField:
    """Represents an oil field."""
    total_amount: float  # billion barrels
    extraction_difficulty: float  # 0 to 1
    oil_quality: float  # 0 to 1
    current_amount: float


@dataclass
class GasReserve:
    """Represents a natural gas reserve."""
    total_amount: float  # trillion cubic feet
    extraction_difficulty: float
    current_amount: float


@dataclass
class Forest:
    """Represents a forest area."""
    area: float  # square kilometers
    density: float  # 0 to 1
    current_area: float


class NaturalResources:
    """Manages natural resources of a country."""
    
    def __init__(self, area: float):
        """
        Initialize natural resources based on country area.
        
        Args:
            area: Total land area in square kilometers
        """
        self.minerals: Dict[str, Mineral] = {}
        self.oil_fields: List[OilField] = []
        self.gas_reserves: List[GasReserve] = []
        self.forests: List[Forest] = []
        
        self._generate_minerals(area)
        self._generate_fossil_fuels()
        self._generate_forests(area)
    
    def _generate_minerals(self, area: float):
        """Generate mineral resources."""
        base_area = 100_000  # Reference area for normalization
        mineral_types = ["Stone", "Iron", "Lithium", "Silicon"]
        
        for mineral_type in mineral_types:
            min_reserve = 5_000
            max_reserve = 1_000_000
            
            total_reserves = random.uniform(min_reserve, max_reserve) * (area / base_area)
            yearly_capacity = total_reserves * random.uniform(0.01, 0.05)
            
            self.minerals[mineral_type] = Mineral(
                name=mineral_type,
                total_reserves=total_reserves,
                yearly_extraction_capacity=yearly_capacity,
                current_reserves=total_reserves
            )
    
    def _generate_fossil_fuels(self):
        """Generate oil and natural gas reserves."""
        # Generate multiple oil fields
        num_fields = random.randint(1, 5)
        for _ in range(num_fields):
            total_amount = random.uniform(0, 100)  # billion barrels
            extraction_difficulty = random.uniform(0, 1)
            oil_quality = random.uniform(0.5, 1.0)
            
            self.oil_fields.append(OilField(
                total_amount=total_amount,
                extraction_difficulty=extraction_difficulty,
                oil_quality=oil_quality,
                current_amount=total_amount
            ))
        
        # Generate gas reserves
        num_reserves = random.randint(1, 4)
        for _ in range(num_reserves):
            total_amount = random.uniform(0, 50)  # trillion cubic feet
            extraction_difficulty = random.uniform(0, 1)
            
            self.gas_reserves.append(GasReserve(
                total_amount=total_amount,
                extraction_difficulty=extraction_difficulty,
                current_amount=total_amount
            ))
    
    def _generate_forests(self, area: float):
        """Generate forest resources."""
        num_forests = random.randint(2, 8)
        total_forest_area = area * random.uniform(0.1, 0.4)
        
        for _ in range(num_forests):
            forest_area = total_forest_area / num_forests * random.uniform(0.5, 1.5)
            density = random.uniform(0.3, 0.9)
            
            self.forests.append(Forest(
                area=forest_area,
                density=density,
                current_area=forest_area
            ))
    
    def get_total_forest_area(self) -> float:
        """Get total current forest area."""
        return sum(forest.current_area for forest in self.forests)
    
    def get_total_oil(self) -> float:
        """Get total remaining oil reserves."""
        return sum(field.current_amount for field in self.oil_fields)
    
    def get_total_gas(self) -> float:
        """Get total remaining gas reserves."""
        return sum(reserve.current_amount for reserve in self.gas_reserves)
    
    def get_mineral_abundance(self) -> float:
        """Get total mineral abundance score."""
        return sum(m.current_reserves for m in self.minerals.values()) / 1e6
    
    def get_oil_abundance(self) -> float:
        """Get oil abundance score."""
        return self.get_total_oil() / 100
    
    def get_gas_abundance(self) -> float:
        """Get gas abundance score."""
        return self.get_total_gas() / 50
    
    def get_forest_abundance(self) -> float:
        """Get forest abundance score."""
        return self.get_total_forest_area() / 1000
    
    def simulate_year(self):
        """Simulate resource extraction for one year."""
        # Extract minerals
        for mineral in self.minerals.values():
            extraction = min(mineral.yearly_extraction_capacity, mineral.current_reserves)
            mineral.current_reserves -= extraction
        
        # Extract oil
        for field in self.oil_fields:
            extraction_rate = 0.02 * (1 - field.extraction_difficulty)
            extraction = field.current_amount * extraction_rate
            field.current_amount -= extraction
        
        # Extract gas
        for reserve in self.gas_reserves:
            extraction_rate = 0.03 * (1 - reserve.extraction_difficulty)
            extraction = reserve.current_amount * extraction_rate
            reserve.current_amount -= extraction
        
        # Forest regeneration/depletion
        for forest in self.forests:
            regeneration = forest.area * 0.001
            depletion = forest.current_area * random.uniform(0, 0.02)
            forest.current_area = max(0, min(forest.area, forest.current_area + regeneration - depletion))
