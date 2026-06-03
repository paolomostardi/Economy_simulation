"""
Output system - handles structured logging of simulation results.
"""

import os
from datetime import datetime
from typing import List, Dict
from country import Country


class OutputManager:
    """Manages output of simulation results to structured text files."""
    
    def __init__(self, seed: int, num_countries: int, simulation_years: int):
        self.seed = seed
        self.num_countries = num_countries
        self.simulation_years = simulation_years
        self.version = "1.0.0"
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create output directory if it doesn't exist (in parent directory)
        self.output_dir = os.path.join("..", "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = os.path.join(self.output_dir, f"simulation_{timestamp}.txt")
        
        self.file = None
    
    def write_header(self):
        """Write metadata header to output file."""
        with open(self.output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ECONOMY SIMULATION RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("METADATA\n")
            f.write("-" * 40 + "\n")
            f.write(f"Random Seed: {self.seed}\n")
            f.write(f"Software Version: {self.version}\n")
            f.write(f"Creation Date: {self.creation_date}\n")
            f.write(f"Number of Countries: {self.num_countries}\n")
            f.write(f"Simulation Duration: {self.simulation_years} years\n")
            f.write("\n")
    
    def write_year_summary(self, year: int, countries: List[Country]):
        """Write summary for a specific year."""
        with open(self.output_file, 'a') as f:
            f.write("=" * 80 + "\n")
            f.write(f"YEAR {year}\n")
            f.write("=" * 80 + "\n\n")
            
            # Top GDP countries
            f.write("TOP 10 COUNTRIES BY GDP\n")
            f.write("-" * 40 + "\n")
            sorted_by_gdp = sorted(countries, key=lambda c: c.economy.gdp, reverse=True)[:10]
            for i, country in enumerate(sorted_by_gdp, 1):
                f.write(f"{i:2d}. {country.name:20s} - GDP: ${country.economy.gdp:,.0f}\n")
            f.write("\n")
            
            # Richest by GDP per capita
            f.write("TOP 10 COUNTRIES BY GDP PER CAPITA\n")
            f.write("-" * 40 + "\n")
            sorted_by_gdp_pc = sorted(countries, key=lambda c: c.economy.gdp_per_capita, reverse=True)[:10]
            for i, country in enumerate(sorted_by_gdp_pc, 1):
                f.write(f"{i:2d}. {country.name:20s} - GDP/Capita: ${country.economy.gdp_per_capita:,.0f}\n")
            f.write("\n")
            
            # Most stable countries
            f.write("TOP 10 MOST STABLE COUNTRIES\n")
            f.write("-" * 40 + "\n")
            sorted_by_stability = sorted(countries, key=lambda c: c.stability, reverse=True)[:10]
            for i, country in enumerate(sorted_by_stability, 1):
                f.write(f"{i:2d}. {country.name:20s} - Stability: {country.stability:.1f}\n")
            f.write("\n")
            
            # Most democratic countries
            f.write("TOP 10 MOST DEMOCRATIC COUNTRIES\n")
            f.write("-" * 40 + "\n")
            sorted_by_democracy = sorted(countries, key=lambda c: c.democracy_index, reverse=True)[:10]
            for i, country in enumerate(sorted_by_democracy, 1):
                f.write(f"{i:2d}. {country.name:20s} - Democracy Index: {country.democracy_index:.1f}\n")
            f.write("\n")
            
            # Most unequal countries
            f.write("TOP 10 MOST UNEQUAL COUNTRIES\n")
            f.write("-" * 40 + "\n")
            sorted_by_inequality = sorted(countries, key=lambda c: c.economy.inequality_factor, reverse=True)[:10]
            for i, country in enumerate(sorted_by_inequality, 1):
                f.write(f"{i:2d}. {country.name:20s} - Inequality: {country.economy.inequality_factor:.3f}\n")
            f.write("\n")
            
            # Population statistics
            f.write("POPULATION STATISTICS\n")
            f.write("-" * 40 + "\n")
            total_pop = sum(c.population.total for c in countries)
            avg_pop = total_pop / len(countries)
            f.write(f"Total World Population: {total_pop:,.0f}\n")
            f.write(f"Average Population per Country: {avg_pop:,.0f}\n")
            f.write("\n")
            
            # Economic statistics
            f.write("ECONOMIC STATISTICS\n")
            f.write("-" * 40 + "\n")
            total_gdp = sum(c.economy.gdp for c in countries)
            avg_gdp = total_gdp / len(countries)
            avg_gdp_pc = sum(c.economy.gdp_per_capita for c in countries) / len(countries)
            avg_unemployment = sum(c.economy.unemployment_rate for c in countries) / len(countries)
            avg_corruption = sum(c.corruption for c in countries) / len(countries)
            avg_stability = sum(c.stability for c in countries) / len(countries)
            
            f.write(f"Total World GDP: ${total_gdp:,.0f}\n")
            f.write(f"Average GDP per Country: ${avg_gdp:,.0f}\n")
            f.write(f"Average GDP per Capita: ${avg_gdp_pc:,.0f}\n")
            f.write(f"Average Unemployment Rate: {avg_unemployment:.2f}%\n")
            f.write(f"Average Corruption Level: {avg_corruption:.2f}\n")
            f.write(f"Average Stability: {avg_stability:.2f}\n")
            f.write("\n")
            
            # Resource depletion warnings
            f.write("RESOURCE DEPLETION WARNINGS\n")
            f.write("-" * 40 + "\n")
            depleted_resources = []
            for country in countries:
                for mineral_name, mineral in country.resources.minerals.items():
                    if mineral.reserves < mineral.extraction_capacity * 2:
                        depleted_resources.append(f"{country.name}: {mineral_name} reserves low")
                for i, field in enumerate(country.resources.oil_fields):
                    if field.total_amount < field.total_amount * 0.1:
                        depleted_resources.append(f"{country.name}: Oil field {i+1} nearly depleted")
            
            if depleted_resources:
                for warning in depleted_resources[:10]:
                    f.write(f"  - {warning}\n")
            else:
                f.write("  No significant resource depletion detected.\n")
            f.write("\n")
            
            # Migration flows
            f.write("MIGRATION FLOWS\n")
            f.write("-" * 40 + "\n")
            total_immigration = sum(c.population.total * c.population.immigration_rate for c in countries)
            total_emigration = sum(c.population.total * c.population.emigration_rate for c in countries)
            f.write(f"Total Immigration: {total_immigration:,.0f}\n")
            f.write(f"Total Emigration: {total_emigration:,.0f}\n")
            f.write(f"Net Migration: {total_immigration - total_emigration:,.0f}\n")
            f.write("\n")
