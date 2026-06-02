"""
Geography system - handles geographical characteristics.
"""

import random


class Geography:
    """Manages geographical characteristics of a country."""
    
    def __init__(self):
        # Temperature (Celsius, average annual)
        self.temperature = random.uniform(-5, 35)
        
        # Seismic level (0-10 scale)
        self.seismic_level = random.uniform(0, 8)
        
        # Mountain percentage (0-100% of land area)
        self.mountain_percentage = random.uniform(0, 60)
        
        # Farmable land (percentage of total area)
        self.farmable_land = self._calculate_farmable_land()
        
        # Fresh water availability (cubic meters per capita per year)
        self.fresh_water = self._calculate_fresh_water()
    
    def _calculate_farmable_land(self) -> float:
        """Calculate farmable land based on geography."""
        base_farmable = random.uniform(20, 70)
        
        # Mountains reduce farmable land
        mountain_penalty = self.mountain_percentage * 0.5
        
        # Extreme temperatures reduce farmable land
        if self.temperature < 0 or self.temperature > 30:
            temp_penalty = 10
        else:
            temp_penalty = 0
        
        farmable = base_farmable - mountain_penalty - temp_penalty
        return max(5, min(80, farmable))
    
    def _calculate_fresh_water(self) -> float:
        """Calculate fresh water availability based on geography."""
        # Base water availability
        base_water = random.uniform(1000, 10000)
        
        # Temperature affects water (hotter = less water due to evaporation)
        temp_factor = 1 - (max(0, self.temperature) / 50)
        
        # Mountains can increase water (snow melt, rivers)
        mountain_bonus = self.mountain_percentage * 20
        
        water = base_water * temp_factor + mountain_bonus
        return max(100, water)
