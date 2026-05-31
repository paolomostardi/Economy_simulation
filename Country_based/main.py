"""
Main entry point for the economy simulation.
"""
from simulation import Simulation


def main():
    """Run the economy simulation."""
    # Create simulation with 50 countries
    sim = Simulation(num_countries=50)
    
    # Run for 10 years
    sim.run(years=10)


if __name__ == "__main__":
    main()
