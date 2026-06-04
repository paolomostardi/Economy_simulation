"""
Geography system - handles geographical characteristics of a country.
"""
import random
from dataclasses import dataclass


@dataclass
class Geography:
    """Represents geographical characteristics of a country."""
    temperature: float  # Average temperature in Celsius
    seismic_level: float  # 0 to 100
    mountain_percentage: float  # 0 to 100
    farmable_land: float  # Square kilometers
    fresh_water: float  # Cubic kilometers
    
    def __init__(self, area: float, forest_area: float = 0):
        """
        Initialize geography based on country area.
        
        Args:
            area: Total land area in square kilometers
            forest_area: Total forest area in square kilometers
        """
        self.temperature = random.uniform(-10, 35)
        self.seismic_level = random.uniform(0, 100)
        self.mountain_percentage = random.uniform(0, 80)
        
        # Farmable land reduced by forest area
        available_land = area - forest_area
        self.farmable_land = max(0, available_land * random.uniform(0.3, 0.7))
        
        # Fresh water influenced by geography
        self._generate_fresh_water()
    
    def _generate_fresh_water(self):
        """Generate fresh water access based on geographical characteristics."""
        # More water with moderate temperature and lower seismic activity
        temp_factor = 1.0 - abs(self.temperature - 15) / 50
        seismic_factor = 1.0 - (self.seismic_level / 200)
        
        base_water = random.uniform(10, 500)  # cubic kilometers
        self.fresh_water = base_water * temp_factor * seismic_factor
    
    def get_farmable_land_percent(self) -> float:
        """Get farmable land as percentage of total area."""
        return (self.farmable_land / (self.farmable_land + 1000)) * 100  # Normalized
    
    def get_fresh_water_factor(self) -> float:
        """Get fresh water availability factor (0 to 1)."""
        return min(1.0, self.fresh_water / 500)
