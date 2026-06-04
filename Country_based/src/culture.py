"""
Culture system - handles cultural properties of a country.
"""
import random
from enum import Enum


class EducationSystemType(Enum):
    """Types of education systems."""
    PUBLIC_ONLY = "public_only"
    PRIVATE_ONLY = "private_only"
    MIXED = "mixed"


class Culture:
    """Represents cultural properties of a country."""
    
    def __init__(self):
        self.language_id: int = random.randint(1, 100)
        self.religion_id: int = random.randint(1, 10)
        self.religious_intensity: float = random.uniform(0, 100)
        self.education_system_type: EducationSystemType = random.choice(list(EducationSystemType))
