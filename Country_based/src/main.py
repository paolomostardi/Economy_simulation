"""
Main entry point for the economy simulation.
"""
from simulation import Simulation


def main():
    """Run the economy simulation."""
    # Create simulation with 50 countries for 10 years
    sim = Simulation(num_countries=50, duration=10, seed=42)
    
    # Run simulation
    sim.run()


if __name__ == "__main__":
    main()
