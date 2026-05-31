"""
Simulation mechanics - Handles the main simulation loop and statistics.
"""
from typing import List
from country import Country


class Simulation:
    """Manages the world simulation."""
    
    def __init__(self, num_countries: int = 50):
        self.countries: List[Country] = []
        self.year: int = 1
        self._generate_countries(num_countries)
    
    def _generate_countries(self, num_countries: int):
        """Generate initial countries."""
        for i in range(num_countries):
            name = f"Country_{i+1}"
            self.countries.append(Country(name))
    
    def simulate_year(self):
        """Simulate one year for all countries."""
        print(f"\n{'='*60}")
        print(f"YEAR {self.year}")
        print(f"{'='*60}")
        
        for country in self.countries:
            country.simulate_year(self.year)
        
        self._print_statistics()
        self.year += 1
    
    def _print_statistics(self):
        """Print yearly statistics."""
        # Sort by GDP
        sorted_by_gdp = sorted(self.countries, key=lambda c: c.gdp, reverse=True)
        
        print("\n--- Top 10 Countries by GDP ---")
        for i, country in enumerate(sorted_by_gdp[:10], 1):
            print(f"{i}. {country.get_summary()}")
        
        # Sort by GDP per capita
        sorted_by_per_capita = sorted(
            self.countries, 
            key=lambda c: c.gdp / c.population * 1e9, 
            reverse=True
        )
        
        print("\n--- Top 10 Richest by GDP per Capita ---")
        for i, country in enumerate(sorted_by_per_capita[:10], 1):
            per_capita = country.gdp / country.population * 1e9
            print(f"{i}. {country.name}: ${per_capita:,.2f} per person")
        
        # Sort by inequality (disparity factor)
        sorted_by_inequality = sorted(
            self.countries,
            key=lambda c: c.population_manager.disparity_factor,
            reverse=True
        )
        
        print("\n--- Top 10 Most Unequal Countries ---")
        for i, country in enumerate(sorted_by_inequality[:10], 1):
            disparity = country.population_manager.disparity_factor
            print(f"{i}. {country.name}: {disparity:.2%} inequality")
        
        # Resource depletion warnings
        print("\n--- Resource Depletion Warnings ---")
        for country in self.countries:
            warnings = []
            
            # Check minerals
            for mineral_name, mineral in country.resource_manager.minerals.items():
                if mineral.current_reserves < mineral.total_reserves * 0.2:
                    warnings.append(f"{mineral_name} at {mineral.current_reserves/mineral.total_reserves:.1%}")
            
            # Check oil
            total_oil = country.resource_manager.get_total_oil()
            if total_oil < 10:  # Less than 10 billion barrels
                warnings.append(f"Oil low ({total_oil:.1f}B barrels)")
            
            # Check forests
            forest_ratio = country.resource_manager.get_total_forest_area() / sum(f.area for f in country.resource_manager.forests)
            if forest_ratio < 0.5:
                warnings.append(f"Forests at {forest_ratio:.1%}")
            
            if warnings:
                print(f"{country.name}: {', '.join(warnings)}")
        
        # World statistics
        total_gdp = sum(c.gdp for c in self.countries)
        total_pop = sum(c.population for c in self.countries)
        avg_stability = sum(c.stability for c in self.countries) / len(self.countries)
        
        print(f"\n--- World Statistics ---")
        print(f"Total GDP: ${total_gdp:,.2f}B")
        print(f"Total Population: {total_pop:,}")
        print(f"Average Stability: {avg_stability:.1f}")
    
    def run(self, years: int = 10):
        """Run the simulation for a specified number of years."""
        print(f"Starting simulation with {len(self.countries)} countries for {years} years...")
        
        for _ in range(years):
            self.simulate_year()
        
        print(f"\n{'='*60}")
        print("Simulation complete!")
        print(f"{'='*60}")
