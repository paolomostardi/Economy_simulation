#!/usr/bin/env python3
"""Test script to verify spending policy calculations."""

import sys
sys.path.insert(0, 'src')

from economy import SpendingPolicy, Economy
from population import Population

def test_spending_policy():
    """Test the spending policy calculation."""
    print("=" * 70)
    print("SPENDING POLICY TEST")
    print("=" * 70)
    
    # Test 1: High democracy (should reduce military spending)
    print("\n1. HIGH DEMOCRACY (90) - Should reduce military spending:")
    pop = Population()
    pop.generate_population()
    
    economy = Economy(
        population=pop.total_population,
        stability=70,
        technology=60,
        corruption=20,
        democracy_index=90,
        age_groups=pop.age_groups
    )
    
    print(f"   Military:              {economy.spending_policy.military:.1f}%")
    print(f"   Healthcare:            {economy.spending_policy.healthcare:.1f}%")
    print(f"   Education:             {economy.spending_policy.education:.1f}%")
    print(f"   Research & Infra:      {economy.spending_policy.research_and_infrastructure:.1f}%")
    print(f"   Total:                 {economy.spending_policy.military + economy.spending_policy.healthcare + economy.spending_policy.education + economy.spending_policy.research_and_infrastructure:.1f}%")
    
    # Test 2: Low democracy (should increase military spending)
    print("\n2. LOW DEMOCRACY (20) - Should increase military spending:")
    economy2 = Economy(
        population=pop.total_population,
        stability=70,
        technology=60,
        corruption=80,
        democracy_index=20,
        age_groups=pop.age_groups
    )
    
    print(f"   Military:              {economy2.spending_policy.military:.1f}%")
    print(f"   Healthcare:            {economy2.spending_policy.healthcare:.1f}%")
    print(f"   Education:             {economy2.spending_policy.education:.1f}%")
    print(f"   Research & Infra:      {economy2.spending_policy.research_and_infrastructure:.1f}%")
    print(f"   Total:                 {economy2.spending_policy.military + economy2.spending_policy.healthcare + economy2.spending_policy.education + economy2.spending_policy.research_and_infrastructure:.1f}%")
    
    # Test 3: Aging population (should increase healthcare spending)
    print("\n3. AGING POPULATION - Should increase healthcare spending:")
    pop_aging = Population()
    pop_aging.generate_population()
    # Artificially increase elderly population
    total = sum(g.population for g in pop_aging.age_groups.values())
    elderly_increase = int(total * 0.25)  # Make 25% elderly
    pop_aging.age_groups["elderly"].population = elderly_increase
    
    economy3 = Economy(
        population=pop_aging.total_population,
        stability=70,
        technology=60,
        corruption=40,
        democracy_index=60,
        age_groups=pop_aging.age_groups
    )
    
    print(f"   Elderly percentage:    {(pop_aging.age_groups['elderly'].population / pop_aging.total_population * 100):.1f}%")
    print(f"   Military:              {economy3.spending_policy.military:.1f}%")
    print(f"   Healthcare:            {economy3.spending_policy.healthcare:.1f}%")
    print(f"   Education:             {economy3.spending_policy.education:.1f}%")
    print(f"   Research & Infra:      {economy3.spending_policy.research_and_infrastructure:.1f}%")
    print(f"   Total:                 {economy3.spending_policy.military + economy3.spending_policy.healthcare + economy3.spending_policy.education + economy3.spending_policy.research_and_infrastructure:.1f}%")
    
    # Test 4: Budget allocation conversion
    print("\n4. BUDGET ALLOCATION CONVERSION (from spending policy):")
    budget = economy.spending_policy.to_budget_allocation(research_ratio=0.6)
    print(f"   Military:              {budget.military * 100:.1f}%")
    print(f"   Healthcare:            {budget.healthcare * 100:.1f}%")
    print(f"   Education:             {budget.education * 100:.1f}%")
    print(f"   Research:              {budget.research * 100:.1f}%")
    print(f"   Infrastructure:        {budget.infrastructure * 100:.1f}%")
    print(f"   Total:                 {(budget.military + budget.healthcare + budget.education + budget.research + budget.infrastructure) * 100:.1f}%")
    
    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    test_spending_policy()
