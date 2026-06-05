# Budget Allocation System - Quick Reference

## TL;DR

The budget system allocates government spending across 4 categories (Military, Healthcare, Education, Research & Infrastructure) that always sum to 100%.

- **Democracy Index** → Affects Military spending (high democracy = less military)
- **Age Distribution** → Affects Healthcare spending (older population = more healthcare)
- **Random Factors** → Creates natural diversity between countries
- **Self-Balancing** → Always sums to exactly 100%, no manual normalization needed

## Core Classes

### SpendingPolicy
4-category budget representation:
```python
spending_policy = SpendingPolicy(
    military=22.5,
    healthcare=31.2,
    education=23.1,
    research_and_infrastructure=23.2
)
```

### BudgetAllocation
5-category budget representation:
```python
budget = BudgetAllocation(
    military=0.225,
    healthcare=0.312,
    education=0.231,
    research=0.139,
    infrastructure=0.093
)
```

## Key Methods

### Calculate Spending Policy
```python
spending_policy = economy.calculate_spending_policy(
    democracy_index=85,
    age_groups=population.age_groups
)
```

### Convert to Budget Allocation
```python
budget = spending_policy.to_budget_allocation(research_ratio=0.6)
# research_ratio: 0-1, how much of research_and_infrastructure goes to research
```

## Effects Summary

| Factor | Category | Effect | Range |
|--------|----------|--------|-------|
| Democracy | Military | High democracy → less military | -15% to +15% |
| Age | Healthcare | Older population → more healthcare | 0% to +20% |
| Random | All | Unique variation per country | ±10% |

## Spending Policy Examples

### Democratic Country (Democracy 90, 10% elderly)
- Military: ~20%
- Healthcare: ~26%
- Education: ~27%
- Research & Infra: ~27%

### Authoritarian Country (Democracy 20, 10% elderly)
- Military: ~32%
- Healthcare: ~24%
- Education: ~22%
- Research & Infra: ~22%

### Aging Democracy (Democracy 80, 30% elderly)
- Military: ~18%
- Healthcare: ~35%
- Education: ~24%
- Research & Infra: ~23%

## Accessing Spending Data

```python
country = Country("MyCountry", 1)

# 4-category spending policy
military_pct = country.economy.spending_policy.military
healthcare_pct = country.economy.spending_policy.healthcare

# 5-category budget allocation
budget = country.economy.spending_policy.to_budget_allocation()
research_pct = budget.research * 100

# Absolute spending amounts (after yearly_update)
military_spending = country.economy.military_spending
healthcare_spending = country.economy.healthcare_spending
```

## Yearly Update

Spending policy is recalculated each year:

```python
country.simulate_year(year=1)
# Inside: economy.yearly_update() recalculates spending_policy
# based on current democracy_index and age_groups
```

## Design Principles

✅ **Self-balancing** - Always sums to 100%
✅ **Dynamic** - Changes yearly with country conditions
✅ **Realistic** - Democracy and demographics drive priorities
✅ **Diverse** - Random factors create unique countries
✅ **Transparent** - Clear formulas and effects
✅ **Reusable** - SpendingPolicy can be used elsewhere

## Files

- `src/economy.py` - Implementation
- `BUDGET_ALLOCATION_SYSTEM.md` - Detailed documentation
- `BUDGET_FORMULAS.md` - Mathematical formulas
- `test_spending_policy.py` - Test suite
- `QUICK_REFERENCE.md` - This file

## Testing

Run tests:
```bash
python test_spending_policy.py
```

Run full simulation:
```bash
python src/main.py
```
