"""
Simulation class - manages the world simulation loop.
"""
import random
from typing import List, Dict
from country import Country
from output import OutputManager


class Simulation:
    """Manages the world simulation."""
    
    def __init__(self, num_countries: int = 50, duration: int = 10, seed: int = None):
        self.num_countries = num_countries
        self.duration = duration
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
        
        self.countries: List[Country] = []
        self.year: int = 1
        self.output_manager = OutputManager()
        
        self._generate_countries()
        self.output_manager.write_metadata(num_countries, duration, seed)
    
    def _generate_countries(self):
        """Generate initial countries."""
        # Load country names from file
        names = self._load_country_names()
        
        for i in range(self.num_countries):
            if i < len(names):
                name = names[i]
            else:
                name = f"Country_{i+1}"  # Fallback if not enough names
            self.countries.append(Country(name, i))
    
    def _load_country_names(self) -> List[str]:
        """Load country names from names.txt file."""
        try:
            with open("names.txt", "r") as f:
                names = [line.strip() for line in f if line.strip()]
            random.shuffle(names)  # Randomize the order
            return names
        except FileNotFoundError:
            print("Warning: names.txt not found, using default names")
            return []
    
    def simulate_year(self):
        """Simulate one year for all countries."""
        # Simulate each country
        for country in self.countries:
            country.simulate_year(self.year)
        
        # Calculate world statistics
        world_stats = {
            "total_gdp": sum(c.economy.gdp for c in self.countries),
            "total_population": sum(c.population.total_population for c in self.countries),
            "avg_stability": sum(c.stability for c in self.countries) / len(self.countries)
        }
        
        # Log critical events
        self._log_events()
        
        # Write outputs
        self.output_manager.write_yearly_csv(self.year, self.countries)
        self.output_manager.write_yearly_json(self.year, self.countries)
        self.output_manager.write_summary(self.year, self.countries, world_stats)
        
        # Print to console
        self._print_console_summary(world_stats)
        
        self.year += 1
    
    def _log_events(self):
        """Log notable events for the year."""
        for country in self.countries:
            # Stability crisis
            if country.stability < 20:
                self.output_manager.log_event(
                    "CRITICAL",
                    country.name,
                    f"Stability crisis at {country.stability:.1f}",
                    self.year
                )
            
            # Resource depletion
            if country.resources.get_total_oil() < 5:
                self.output_manager.log_event(
                    "WARNING",
                    country.name,
                    f"Oil reserves depleted ({country.resources.get_total_oil():.1f}B barrels)",
                    self.year
                )
            
            # GDP collapse
            if country.economy.gdp_growth_rate < -0.1:
                self.output_manager.log_event(
                    "CRITICAL",
                    country.name,
                    f"GDP collapsed by {country.economy.gdp_growth_rate*100:.1f}%",
                    self.year
                )
            
            # Food shortage
            if country.industries.food_ratio < 0.5:
                self.output_manager.log_event(
                    "WARNING",
                    country.name,
                    f"Food shortage ({country.industries.food_ratio:.1%} of demand)",
                    self.year
                )
    
    def _print_console_summary(self, world_stats: Dict):
        """Print brief console summary."""
        print(f"\nYear {self.year} | World GDP: ${world_stats['total_gdp']/1e9:,.2f}B | "
              f"Population: {world_stats['total_population']:,} | "
              f"Avg Stability: {world_stats['avg_stability']:.1f}")
        
        # Top 5 GDP
        sorted_by_gdp = sorted(self.countries, key=lambda c: c.economy.gdp, reverse=True)
        print("Top 5 GDP:", ", ".join(f"{c.name} (${c.economy.gdp/1e9:.1f}B)" for c in sorted_by_gdp[:5]))
    
    def run(self):
        """Run the complete simulation."""
        print(f"Starting simulation with {self.num_countries} countries for {self.duration} years...")
        if self.seed is not None:
            print(f"Random seed: {self.seed}")
        
        for _ in range(self.duration):
            self.simulate_year()
        
        # Write final events
        self.output_manager.write_events()
        
        print(f"\nSimulation complete!")
        print(f"Output written to {self.output_manager.output_dir}")
