"""
Resource management - Handles natural resources including minerals, fossil fuels, wood, and geography.
"""
import random
import math
from typing import Dict, List
from dataclasses import dataclass


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


@dataclass
class Geography:
    """Represents geographical characteristics."""
    temperature: float  # average temperature in Celsius
    seismic_level: float  # 0 to 100
    mountain_percentage: float  # 0 to 100
    farmable_land: float  # square kilometers


class ResourceManager:
    """Manages natural resources and geographical characteristics."""
    
    def __init__(self):
        self.minerals: Dict[str, Mineral] = {}
        self.oil_fields: List[OilField] = []
        self.gas_reserves: List[GasReserve] = []
        self.forests: List[Forest] = []
        self.geography: Geography = None
        self.fresh_water: float = 0.0  # cubic kilometers
    
    def generate_resources(self, area: float):
        """Generate all resources based on country area."""
        self._generate_minerals(area)
        self._generate_fossil_fuels(area)
        self._generate_forests(area)
        self._generate_geography(area)
        self._generate_fresh_water()
    
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
    
    def _generate_fossil_fuels(self, area: float):
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
    
    def _generate_geography(self, area: float):
        """Generate geographical characteristics."""
        temperature = random.uniform(-10, 35)  # Celsius
        seismic_level = random.uniform(0, 100)
        mountain_percentage = random.uniform(0, 80)
        
        # Farmable land reduced by forest area
        total_forest_area = sum(f.area for f in self.forests)
        farmable_land = (area - total_forest_area) * random.uniform(0.3, 0.7)
        farmable_land = max(0, farmable_land)
        
        self.geography = Geography(
            temperature=temperature,
            seismic_level=seismic_level,
            mountain_percentage=mountain_percentage,
            farmable_land=farmable_land
        )
    
    def _generate_fresh_water(self):
        """Generate fresh water access based on geography."""
        # More water with moderate temperature and lower seismic activity
        temp_factor = 1.0 - abs(self.geography.temperature - 15) / 50
        seismic_factor = 1.0 - (self.geography.seismic_level / 200)
        
        base_water = random.uniform(10, 500)  # cubic kilometers
        self.fresh_water = base_water * temp_factor * seismic_factor
    
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
            # Small regeneration
            regeneration = forest.area * 0.001
            # Depletion from logging
            depletion = forest.current_area * random.uniform(0, 0.02)
            forest.current_area = max(0, min(forest.area, forest.current_area + regeneration - depletion))
    
    def get_total_oil(self) -> float:
        """Get total remaining oil reserves."""
        return sum(field.current_amount for field in self.oil_fields)
    
    def get_total_gas(self) -> float:
        """Get total remaining gas reserves."""
        return sum(reserve.current_amount for reserve in self.gas_reserves)
    
    def get_total_forest_area(self) -> float:
        """Get total current forest area."""
        return sum(forest.current_area for forest in self.forests)
