"""
Output system - handles writing simulation results to files.
"""
import json
import csv
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class OutputManager:
    """Manages simulation output to various file formats."""
    
    def __init__(self, output_dir: str = "output"):
        # Create timestamped folder for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(output_dir) / timestamp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.output_dir / "metadata.json"
        self.summary_file = self.output_dir / "world_summary.txt"
        self.csv_file = self.output_dir / "yearly_data.csv"
        self.json_file = self.output_dir / "yearly_data.json"
        self.event_file = self.output_dir / "events.log"
        
        self.events: List[str] = []
        self.yearly_data: List[Dict] = []
    
    def write_metadata(self, num_countries: int, duration: int, seed: int = None):
        """Write simulation metadata."""
        metadata = {
            "random_seed": seed,
            "software_version": "1.0.0",
            "creation_date": datetime.now().isoformat(),
            "number_of_countries": num_countries,
            "simulation_duration": duration,
            "configuration": {
                "num_countries": num_countries,
                "duration_years": duration
            }
        }
        
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def log_event(self, severity: str, country_name: str, description: str, year: int):
        """Log an event to the event file."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        event = f"[{timestamp}] [Year {year}] [{severity}] {country_name}: {description}"
        self.events.append(event)
    
    def write_events(self):
        """Write all events to the event log file."""
        with open(self.event_file, 'w') as f:
            for event in self.events:
                f.write(event + "\n")
    
    def write_yearly_csv(self, year: int, countries: List):
        """Write yearly data to CSV file."""
        if year == 1:
            # Write header
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "year", "country_id", "country_name", "population", "gdp", "gdp_per_capita",
                    "stability", "democracy", "corruption", "unemployment", "net_migration",
                    "birth_rate", "death_rate", "inflation", "resource_reserve_index"
                ])
        
        # Write data
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            for country in countries:
                data = country.to_dict()
                writer.writerow([
                    year,
                    data["id"],
                    data["name"],
                    data["population"],
                    f"{data['gdp']:.2f}",
                    f"{data['gdp_per_capita']:.2f}",
                    f"{data['stability']:.2f}",
                    f"{data['democracy']:.2f}",
                    f"{data['corruption']:.2f}",
                    f"{data['unemployment']:.2f}",
                    data["net_migration"],
                    f"{data['birth_rate']:.4f}",
                    f"{data['death_rate']:.4f}",
                    f"{data['inflation']:.4f}",
                    f"{data['resource_reserve_index']:.2f}"
                ])
    
    def write_yearly_json(self, year: int, countries: List):
        """Write yearly data to JSON file."""
        year_data = {
            "year": year,
            "countries": [country.to_dict() for country in countries]
        }
        self.yearly_data.append(year_data)
        
        with open(self.json_file, 'w') as f:
            json.dump(self.yearly_data, f, indent=2)
    
    def write_summary(self, year: int, countries: List, world_stats: Dict):
        """Write human-readable summary."""
        with open(self.summary_file, 'a') as f:
            # Year header
            f.write(f"\n{'='*80}\n")
            f.write(f"Year {year} | World GDP: ${world_stats['total_gdp']/1e9:,.2f}B | ")
            f.write(f"World Population: {world_stats['total_population']:,} | ")
            f.write(f"Avg Stability: {world_stats['avg_stability']:.1f}\n")
            f.write(f"{'='*80}\n")
            
            # Top 5 highlights
            f.write("\n--- Top 5 Highlights ---\n")
            highlights = self._generate_highlights(countries, year)
            for i, highlight in enumerate(highlights, 1):
                f.write(f"{i}. {highlight}\n")
            
            # Ranked lists
            f.write("\n--- Top 10 Countries by GDP ---\n")
            sorted_by_gdp = sorted(countries, key=lambda c: c.economy.gdp, reverse=True)
            for i, country in enumerate(sorted_by_gdp[:10], 1):
                f.write(f"{i}. {country.get_summary()}\n")
            
            f.write("\n--- Top 10 Richest by GDP per Capita ---\n")
            sorted_by_per_capita = sorted(countries, key=lambda c: c.economy.gdp_per_capita, reverse=True)
            for i, country in enumerate(sorted_by_per_capita[:10], 1):
                f.write(f"{i}. {country.name}: ${country.economy.gdp_per_capita:,.2f} per person\n")
            
            f.write("\n--- Top 10 Most Stable ---\n")
            sorted_by_stability = sorted(countries, key=lambda c: c.stability, reverse=True)
            for i, country in enumerate(sorted_by_stability[:10], 1):
                f.write(f"{i}. {country.name}: {country.stability:.1f}\n")
            
            f.write("\n--- Top 10 Most Democratic ---\n")
            sorted_by_democracy = sorted(countries, key=lambda c: c.democracy_index, reverse=True)
            for i, country in enumerate(sorted_by_democracy[:10], 1):
                f.write(f"{i}. {country.name}: {country.democracy_index:.1f}\n")
            
            f.write("\n--- Top 10 Most Unequal ---\n")
            sorted_by_inequality = sorted(countries, key=lambda c: c.population.disparity_factor, reverse=True)
            for i, country in enumerate(sorted_by_inequality[:10], 1):
                f.write(f"{i}. {country.name}: {country.population.disparity_factor:.2%} inequality\n")
            
            # Notable events
            year_events = [e for e in self.events if f"[Year {year}]" in e]
            if year_events:
                f.write("\n--- Notable Events ---\n")
                for event in year_events:
                    f.write(f"{event}\n")
            
            # Migration summary
            f.write("\n--- Migration Summary ---\n")
            total_immigration = sum(c.population.net_migration for c in countries if c.population.net_migration > 0)
            total_emigration = sum(abs(c.population.net_migration) for c in countries if c.population.net_migration < 0)
            f.write(f"Net global immigration: {total_immigration:,}\n")
            f.write(f"Net global emigration: {total_emigration:,}\n")
            
            highest_immigration = sorted(countries, key=lambda c: c.population.net_migration, reverse=True)[:3]
            f.write("Highest immigration: ")
            f.write(", ".join(f"{c.name} ({c.population.net_migration:,})" for c in highest_immigration))
            f.write("\n")
            
            highest_emigration = sorted(countries, key=lambda c: c.population.net_migration)[:3]
            f.write("Highest emigration: ")
            f.write(", ".join(f"{c.name} ({c.population.net_migration:,})" for c in highest_emigration))
            f.write("\n")
            
            # Resource warnings
            f.write("\n--- Resource Warnings ---\n")
            warnings = self._generate_resource_warnings(countries)
            if warnings:
                for warning in warnings:
                    f.write(f"{warning}\n")
            else:
                f.write("No critical resource depletion warnings.\n")
    
    def _generate_highlights(self, countries: List, year: int) -> List[str]:
        """Generate top 5 highlights for the year."""
        highlights = []
        
        # Find GDP leaders
        sorted_by_gdp = sorted(countries, key=lambda c: c.economy.gdp, reverse=True)
        if sorted_by_gdp:
            top_gdp = sorted_by_gdp[0]
            highlights.append(f"{top_gdp.name} leads with ${top_gdp.economy.gdp/1e9:.2f}B GDP")
        
        # Find fastest growing
        sorted_by_growth = sorted(countries, key=lambda c: c.economy.gdp_growth_rate, reverse=True)
        if sorted_by_growth and sorted_by_growth[0].economy.gdp_growth_rate > 0.05:
            highlights.append(f"{sorted_by_growth[0].name} grew by {sorted_by_growth[0].economy.gdp_growth_rate*100:.1f}%")
        
        # Find stability crisis
        crisis_countries = [c for c in countries if c.stability < 30]
        if crisis_countries:
            highlights.append(f"{len(crisis_countries)} countries in stability crisis")
        
        # Find resource depletion
        depleted = [c for c in countries if c.resources.get_total_oil() < 5]
        if depleted:
            highlights.append(f"{len(depleted)} countries facing oil depletion")
        
        # Find population growth
        sorted_by_pop_growth = sorted(countries, key=lambda c: c.population.total_population, reverse=True)
        if sorted_by_pop_growth:
            highlights.append(f"World population: {sum(c.population.total_population for c in countries):,}")
        
        return highlights[:5]
    
    def _generate_resource_warnings(self, countries: List) -> List[str]:
        """Generate resource depletion warnings."""
        warnings = []
        
        for country in countries:
            # Check oil
            total_oil = country.resources.get_total_oil()
            if total_oil < 10:
                warnings.append(f"[WARNING] {country.name}: Oil reserves low ({total_oil:.1f}B barrels)")
            
            # Check minerals
            for mineral_name, mineral in country.resources.minerals.items():
                if mineral.current_reserves < mineral.total_reserves * 0.2:
                    warnings.append(f"[WARNING] {country.name}: {mineral_name} at {mineral.current_reserves/mineral.total_reserves:.1%}")
            
            # Check forests
            forest_ratio = country.resources.get_total_forest_area() / sum(f.area for f in country.resources.forests)
            if forest_ratio < 0.5:
                warnings.append(f"[WARNING] {country.name}: Forests at {forest_ratio:.1%}")
        
        return warnings[:20]  # Limit to 20 warnings
