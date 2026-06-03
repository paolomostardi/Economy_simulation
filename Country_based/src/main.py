"""
Main entry point for the economy simulation.
"""

import random
from datetime import datetime
from typing import List

from country import Country
from output import OutputManager


def generate_country_name(index: int) -> str:
    """Generate a unique country name."""
    prefixes = ["North", "South", "East", "West", "New", "Great", "United", "Democratic", "Federal", "Republic"]
    suffixes = ["land", "ia", "stan", "burg", "ville", "ton", "field", "gard", "haven", "port"]
    
    if index < 20:
        return f"{prefixes[index % len(prefixes)]}{suffixes[index % len(suffixes)]}"
    else:
        return f"Country_{index}"


def main():
    """Main simulation loop."""
    # Set random seed for reproducibility
    seed = random.randint(0, 1000000)
    random.seed(seed)
    
    # Configuration
    num_countries = 50
    simulation_years = 10
    
    # Create output manager
    output = OutputManager(seed, num_countries, simulation_years)
    
    # Generate countries
    countries: List[Country] = []
    for i in range(num_countries):
        name = generate_country_name(i)
        country = Country(name)
        countries.append(country)
    
    # Write initial state
    output.write_header()
    output.write_year_summary(0, countries)
    
    # Run simulation
    for year in range(1, simulation_years + 1):
        print(f"Simulating year {year}...")
        
        for country in countries:
            country.yearly_update()
        
        output.write_year_summary(year, countries)
    
    print(f"\nSimulation complete. Results written to {output.output_file}")


if __name__ == "__main__":
    main()
