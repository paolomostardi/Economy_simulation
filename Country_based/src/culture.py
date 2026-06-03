"""
Culture system - handles cultural attributes and education.
"""

import random
from enum import Enum


class EducationSystem(Enum):
    """Types of education systems."""
    PUBLIC_ONLY = "Public only"
    PRIVATE_ONLY = "Private only"
    MIXED = "Mixed"


class Culture:
    """Manages cultural attributes and education."""
    
    def __init__(self):
        # Language ID (1-100)
        self.language_id = random.randint(1, 100)
        
        # Religion ID (1-10)
        self.religion_id = random.randint(1, 10)
        
        # Religious intensity (0-100)
        self.religious_intensity = random.uniform(0, 100)
        
        # Education scores (0-100)
        self.technical_education = random.uniform(20, 80)
        self.cultural_education = random.uniform(20, 80)
        
        # Education system type
        self.education_system = self._generate_education_system()
    
    def _generate_education_system(self) -> EducationSystem:
        """Generate education system type."""
        rand = random.random()
        if rand < 0.4:
            return EducationSystem.PUBLIC_ONLY
        elif rand < 0.7:
            return EducationSystem.MIXED
        else:
            return EducationSystem.PRIVATE_ONLY
